import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

BIO_CSV = r"C:\Users\pirnu\mat_ecg_gsr_synced_Verda.csv"
MAT_CSV = r"C:\Users\pirnu\MAT_Verda.csv"

TIME_COL="new_time"; ECG_COL="ecg_value_num"; GSR_COL="gsr_value_num"
R_COL="routine"; N_COL="thisN"; ANS_COL="answer"; USER_COL="user_answer"

FS=250.0; LOWCUT=5; HIGHCUT=20; ORDER=2; MIN_BEAT_SEC=0.35; K_STD=2.0
PARTS=["part1","part2","part3"]

num = lambda s: pd.to_numeric(s, errors="coerce")

def pick_time_cols(df):
    starts=["timestampStart","timestamp_start","start_time","t_start"]
    ends  =["timestampEnd","timestamp_end","end_time","t_end"]
    s = next((c for c in starts if c in df.columns), None)
    e = next((c for c in ends   if c in df.columns), None)
    return s, e

def add_bar_numbers(ax, bars):
    for b in bars:
        h = b.get_height()
        if h <= 0 or (not np.isfinite(h)):
            continue
        ax.text(b.get_x()+b.get_width()/2, h, f"{int(h)}", ha="center", va="bottom", fontsize=9)

def get_resting2_from_bio(bio_df, time_col, routine_col="routine"):
    """BIO içindeki routine kolonundan RESTING2 segmentinin t0/t1'ini bulur (min/max)."""
    if routine_col not in bio_df.columns:
        return None

    r = bio_df[routine_col].astype(str).str.strip().str.lower()
    r = r.replace(["nan", "none", ""], "unknown")

    m = r.str.contains(r"rest\s*2|resting\s*2|rest_?2|resting2|rest2", regex=True, na=False)
    if not m.any():
        return None

    sub = bio_df.loc[m, [time_col]].dropna()
    if sub.empty:
        return None

    t0 = float(sub[time_col].min())
    t1 = float(sub[time_col].max())
    if t1 <= t0:
        return None
    return (t0, t1)


mat=pd.read_csv(MAT_CSV, low_memory=False)
mat[R_COL]=mat[R_COL].astype(str).str.strip().str.lower()
mat[N_COL]=num(mat[N_COL]); mat[ANS_COL]=num(mat[ANS_COL])

ua=mat[USER_COL].astype(str).str.strip().str.lower()
mat["timeout"]=ua.eq("none")
mat["user_num"]=num(ua.where(~mat["timeout"], np.nan))

S_COL,E_COL=pick_time_cols(mat)
if E_COL is None:
    raise ValueError("MAT end time kolonu yok (timestampEnd vb.)")

mat[E_COL]=num(mat[E_COL])
if np.nanmedian(mat[E_COL])>1e6:
    mat[E_COL]=mat[E_COL]/1000.0

if S_COL:
    mat[S_COL]=num(mat[S_COL])
    if np.nanmedian(mat[S_COL])>1e6:
        mat[S_COL]=mat[S_COL]/1000.0

base=mat[mat[R_COL].str.contains("baseline", na=False)]
if base.empty:
    raise ValueError("MAT içinde baseline yok")
if (S_COL is None) or base[S_COL].dropna().empty:
    raise ValueError("MAT baseline start gerekli (timestampStart vb.)")

base_start=float(base[S_COL].dropna().iloc[0])
base_end  =float(base[E_COL].dropna().iloc[0])
baseline_dur=base_end-base_start
if baseline_dur<=0:
    raise ValueError("baseline dur hatalı")

rel=lambda x: float(x-base_start)


bio = pd.read_csv(BIO_CSV, low_memory=False)
bio[TIME_COL]=num(bio[TIME_COL])
bio[ECG_COL]=num(bio[ECG_COL]).interpolate(limit_direction="both")
bio[GSR_COL]=num(bio[GSR_COL]).interpolate(limit_direction="both")
bio=bio.dropna(subset=[TIME_COL]).sort_values(TIME_COL).reset_index(drop=True)

t=bio[TIME_COL].to_numpy(float)


if np.nanmedian(t) > 1e6:
    t = t / 1000.0


if np.nanmedian(t) > 1e6:
    t = t - base_start


ecg=bio[ECG_COL].to_numpy(float)
gsr=bio[GSR_COL].to_numpy(float)

nyq=0.5*FS
b,a=butter(ORDER,[LOWCUT/nyq,HIGHCUT/nyq],btype="band")
ecg_f=filtfilt(b,a,ecg)
min_dist=int(MIN_BEAT_SEC*FS)

# =========================================================
#  MAT'ten Level1/Level2 soru zamanları (t0,t1)
# =========================================================
q=mat[mat[N_COL].notna()].copy()
q=q[q[R_COL].isin(["level1","level2"])].dropna(subset=[E_COL]).sort_values([R_COL,N_COL])
q["t1"]=q[E_COL].apply(rel)

def build_times(routine):
    sub=q[q[R_COL]==routine].copy()
    if sub.empty:
        return sub
    if (S_COL is not None) and sub[S_COL].notna().any():
        sub=sub.dropna(subset=[S_COL]).copy()
        sub["t0"]=sub[S_COL].apply(rel)
        sub["t1"]=sub[E_COL].apply(rel)
    else:
        prev=baseline_dur
        t0=[]
        for t1_ in sub["t1"].to_list():
            t0.append(prev); prev=float(t1_)
        sub["t0"]=t0
    return sub[[R_COL,N_COL,"t0","t1",ANS_COL,"user_num","timeout"]]

qq=pd.concat([build_times("level1"), build_times("level2")], ignore_index=True)


def add_parts(df):
    df=df.copy()
    mx=int(df[N_COL].max())
    bins=np.linspace(0,mx,4)
    df["part"]=pd.cut(df[N_COL], bins=bins, labels=PARTS, include_lowest=True)
    return df

qq=qq.groupby(R_COL, group_keys=False).apply(add_parts)

rows=[]
for (r,p),sub in qq.groupby([R_COL,"part"]):
    t0=float(sub["t0"].min()); t1=float(sub["t1"].max())
    if t1<=t0:
        continue

    answered=sub["user_num"].notna()
    correct=answered & (sub["user_num"]==sub[ANS_COL])
    wrong=answered & (~correct)
    timeout=sub["timeout"] | (~answered)

    rows.append({"routine":r,"part":p,"t0":t0,"t1":t1,
                 "correct":int(correct.sum()),"wrong":int(wrong.sum()),"timeout":int(timeout.sum())})

win=pd.DataFrame(rows)


extra_rows=[]


patterns_mat = {
    "baseline": r"baseline",
    "resting1": r"rest\s*1|resting\s*1|rest_?1|resting1|rest1",
}
for label, pat in patterns_mat.items():
    sub = mat[mat[R_COL].astype(str).str.lower().str.contains(pat, regex=True, na=False)]
    if sub.empty or (S_COL is None) or sub[S_COL].dropna().empty or sub[E_COL].dropna().empty:
        continue
    t0=float(rel(sub[S_COL].dropna().min()))
    t1=float(rel(sub[E_COL].dropna().max()))
    if t1<=t0:
        continue
    extra_rows.append({"routine":label,"part":"all","t0":t0,"t1":t1,
                       "correct":0,"wrong":0,"timeout":0})


bio_r2 = get_resting2_from_bio(bio, TIME_COL, routine_col=R_COL)
if bio_r2 is not None:
    t0_bio, t1_bio = bio_r2

   
    t0_tmp = float(t0_bio); t1_tmp = float(t1_bio)
    if np.nanmedian(bio[TIME_COL].to_numpy(float)) > 1e6:
        t0_tmp /= 1000.0; t1_tmp /= 1000.0
    if t0_tmp > 1e6:  # hala epoch ise
        t0_tmp -= base_start; t1_tmp -= base_start

    extra_rows.append({"routine":"resting2","part":"all","t0":t0_tmp,"t1":t1_tmp,
                       "correct":0,"wrong":0,"timeout":0})
else:
    print("[WARN] BIO içinde resting2 bulunamadı. (routine kolonu/isimleri kontrol et)")

if extra_rows:
    win = pd.concat([win, pd.DataFrame(extra_rows)], ignore_index=True)

# Sırala
order_map={"baseline":0,"resting1":1,"resting2":2,"level1":10,"level2":11}
win["_ord"]=win["routine"].map(order_map).fillna(99)
win=win.sort_values(["_ord","part"]).drop(columns=["_ord"]).reset_index(drop=True)

# =========================================================
#  BPM + GSR mean (inside the window)
# =========================================================
def bpm_in_window(t0,t1):
    m=(t>=t0)&(t<=t1)
    n=int(m.sum())
    if n < int(FS*2):
        return np.nan

    seg=ecg_f[m]


    dur=(n-1)/FS
    if dur<=0:
        return np.nan

    thr=float(np.nanmedian(seg)+K_STD*np.nanstd(seg))
    if not np.isfinite(thr):
        return np.nan

    peaks,_=find_peaks(seg, height=thr, distance=min_dist)
    return float(len(peaks)/dur*60.0)

def gsr_mean_in_window(t0,t1):
    m=(t>=t0)&(t<=t1)
    if int(m.sum()) == 0:
        return np.nan
    return float(np.nanmean(gsr[m]))

win["bpm_avg"]=win.apply(lambda r: bpm_in_window(r["t0"],r["t1"]), axis=1)
win["gsr_mean"]=win.apply(lambda r: gsr_mean_in_window(r["t0"],r["t1"]), axis=1)

print("\n=== WIN TABLE ===")
print(win.to_string(index=False))

r2 = win[win["routine"].astype(str).str.lower().eq("resting2")]
if not r2.empty:
    t0r = float(r2.iloc[0]["t0"]); t1r = float(r2.iloc[0]["t1"])
    m = (t>=t0r)&(t<=t1r)
    print("\n[DEBUG] RESTING2 t0,t1,dur:", t0r, t1r, (t1r-t0r))
    print("[DEBUG] RESTING2 m.sum:", int(m.sum()), " | t_min/max:", float(np.nanmin(t)), float(np.nanmax(t)))

# =========================================================
#  Plot
# =========================================================
fig=plt.figure(figsize=(18,9))
gs=fig.add_gridspec(2,2,width_ratios=[2.4,1.2],height_ratios=[1,1],wspace=0.25,hspace=0.25)
ax_bpm=fig.add_subplot(gs[0,0])
ax_gsr=fig.add_subplot(gs[1,0], sharex=ax_bpm)
ax_perf=fig.add_subplot(gs[:,1])

# label
for _,r in win.iterrows():
    for ax in (ax_bpm, ax_gsr):
        ax.axvline(r["t0"], linestyle="--", linewidth=1.0, alpha=0.55)
        ax.axvline(r["t1"], linestyle="--", linewidth=1.0, alpha=0.55)
        ax.text((r["t0"]+r["t1"])/2, 0.98, f"{str(r['routine']).upper()}",
                transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.6, edgecolor="none"))

# BPM mean line
for _,r in win.iterrows():
    if np.isfinite(r["bpm_avg"]):
        ax_bpm.plot([r["t0"],r["t1"]],[r["bpm_avg"],r["bpm_avg"]], linewidth=2.2)
        ax_bpm.text((r["t0"]+r["t1"])/2, r["bpm_avg"], f"{r['bpm_avg']:.1f}",
                    ha="center", va="bottom", fontsize=9)

ax_bpm.set_title("BPM average")
ax_bpm.set_ylabel("BPM")
ax_bpm.grid(True, alpha=0.25)

# GSR waveform + mean
ax_gsr.plot(t, gsr, linewidth=0.8)
for _,r in win.iterrows():
    if np.isfinite(r["gsr_mean"]):
        ax_gsr.plot([r["t0"],r["t1"]],[r["gsr_mean"],r["gsr_mean"]], linewidth=2.0)
        ax_gsr.text((r["t0"]+r["t1"])/2, r["gsr_mean"], f"{r['gsr_mean']:.2f}",
                    ha="center", va="bottom", fontsize=9)

ax_gsr.set_title("GSR waveform")
ax_gsr.set_ylabel("ADC")
ax_gsr.set_xlabel("time")
ax_gsr.grid(True, alpha=0.25)

ax_perf.set_title("MAT Performance")
win_perf = win[win["routine"].isin(["level1","level2"])].reset_index(drop=True)

labels=(win_perf["routine"].str.upper()).to_list()
x=np.arange(len(win_perf)); wbar=0.25

bc = ax_perf.bar(x-wbar, win_perf["correct"], width=wbar, color="#2ca02c", label="Correct")
bw = ax_perf.bar(x,      win_perf["wrong"],   width=wbar, color="#d62728", label="Wrong")
bt = ax_perf.bar(x+wbar, win_perf["timeout"], width=wbar, color="grey",     label="Timeout")

add_bar_numbers(ax_perf, bc); add_bar_numbers(ax_perf, bw); add_bar_numbers(ax_perf, bt)

ax_perf.set_xticks(x)
ax_perf.set_xticklabels(labels, fontsize=10)
ax_perf.set_ylabel("Count")
ax_perf.grid(True, axis="y", alpha=0.25)
ax_perf.legend(loc="upper right")

plt.tight_layout()
plt.show()
