"""
Generate 4 separate PNG visualizations for the Project 2 final HTML submission.
Proposition: "China's economic rise has made meaningful climate progress impossible."
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

# ── Load data ──────────────────────────────────────────────────────────────────
with open('climate-change.csv') as f:
    rows = list(csv.DictReader(f))

def get_series(country, col):
    data = {}
    for r in rows:
        if r['Country Name'] == country and r.get(col):
            try:
                data[int(r['Year'])] = float(r[col])
            except (ValueError, KeyError):
                pass
    return dict(sorted(data.items()))

CO2_KT  = 'average_value_CO2 emissions (kt)'
CO2_CAP = 'average_value_CO2 emissions (metric tons per capita)'
RENEW   = 'average_value_Renewable energy consumption (% of total final energy consumption)'

# Build series
usa_kt    = get_series('United States', CO2_KT)
china_kt  = get_series('China', CO2_KT)
ger_kt    = get_series('Germany', CO2_KT)
uk_kt     = get_series('United Kingdom', CO2_KT)
fra_kt    = get_series('France', CO2_KT)
can_kt    = get_series('Canada', CO2_KT)
jpn_kt    = get_series('Japan', CO2_KT)

usa_cap   = get_series('United States', CO2_CAP)
china_cap = get_series('China', CO2_CAP)
ger_cap   = get_series('Germany', CO2_CAP)
ind_cap   = get_series('India', CO2_CAP)
uk_cap    = get_series('United Kingdom', CO2_CAP)
can_cap   = get_series('Canada', CO2_CAP)
aus_cap   = get_series('Australia', CO2_CAP)

china_renew = get_series('China', RENEW)
ger_renew   = get_series('Germany', RENEW)
usa_renew   = get_series('United States', RENEW)
uk_renew    = get_series('United Kingdom', RENEW)

# ── Colors ─────────────────────────────────────────────────────────────────────
CHINA_RED   = '#8C1C13'
CHINA_DARK  = '#5C120D'
WEST_BLUE   = '#0E4D64'
WEST_LIGHT  = '#5DA9E9'
NEUTRAL     = '#6E7F8D'
BG          = '#F2F0EF'
ACCENT_GOLD = '#E89B2C'
GER_GREEN   = '#A7DCC9'
PANEL_LIGHT = '#F3F7FA'
WEST_DARK   = '#16324F'

DPI = 160


# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 1 — China Erased Every Gain the West Ever Made
# ═══════════════════════════════════════════════════════════════════════════════
def viz1_china_vs_west_emissions():
    fig, ax = plt.subplots(figsize=(9, 6.5), facecolor=BG)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_visible(False)

    years = list(range(1990, 2019))
    west_total = {}
    for y in years:
        total = 0
        for ser in [usa_kt, ger_kt, uk_kt, fra_kt, can_kt, jpn_kt]:
            total += ser.get(y, np.nan)
        west_total[y] = total / 1e6

    china_bil = {y: china_kt.get(y, np.nan) / 1e6 for y in years}
    w_vals = [west_total[y] for y in years]
    c_vals = [china_bil[y] for y in years]

    w_base, c_base = w_vals[0], c_vals[0]
    w_change = [v - w_base for v in w_vals]
    c_change = [v - c_base for v in c_vals]

    ax.fill_between(years, 0, c_change, color=CHINA_RED, alpha=0.85,
                    label='China: added emissions')
    ax.fill_between(years, 0, w_change, color=WEST_BLUE, alpha=0.70,
                    label='West: change in emissions')
    ax.plot(years, c_change, color=CHINA_DARK, lw=2)
    ax.plot(years, w_change, color=WEST_DARK, lw=2)
    ax.axhline(0, color='#7F8C8D', lw=1.2, ls='--', alpha=0.5)

    ax.annotate('+8.1 billion\ntonnes added\nby China',
                xy=(2018, c_change[-1]), xytext=(2008, 6.5),
                color=CHINA_RED, fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=CHINA_RED, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=CHINA_RED, alpha=0.9))

    ax.annotate('West barely\nbudged: −0.2B\ntonnes combined',
                xy=(2018, w_change[-1]), xytext=(1995, 2.2),
                color=WEST_BLUE, fontsize=10,
                arrowprops=dict(arrowstyle='->', color=WEST_BLUE, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=WEST_BLUE, alpha=0.9))

    ax.set_xlim(1990, 2018)
    ax.set_xlabel('Year', color='#2C3E50', fontsize=11)
    ax.set_ylabel('Change from 1990 baseline (billion metric tonnes CO₂)',
                  color='#2C3E50', fontsize=10)
    ax.set_title("China Erased Every Gain the West Ever Made",
                 color='#1A1A2E', fontsize=14, fontweight='bold', pad=14)
    ax.tick_params(colors='#2C3E50', labelsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:+.0f}B'))
    ax.legend(loc='upper left', facecolor='white', edgecolor='#D9E2EC',
              labelcolor='#2C3E50', fontsize=10)

    fig.text(0.5, 0.01,
             '"West" = USA + Germany + UK + France + Canada + Japan combined.  '
             'Baseline: 1990 emissions.  Source: World Bank Climate Change Indicators.',
             ha='center', color='#666', fontsize=8.5, style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('images/viz1_china_vs_west.png', dpi=DPI, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print('Saved viz1_china_vs_west.png')


# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 2 — China's Renewables Share Has Plummeted
# ═══════════════════════════════════════════════════════════════════════════════
def viz2_renewables():
    fig, ax = plt.subplots(figsize=(9, 6.5), facecolor=BG)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_visible(False)

    renew_years = sorted(set(china_renew) & set(ger_renew) & set(uk_renew))
    c_r = [china_renew[y] for y in renew_years]
    g_r = [ger_renew[y] for y in renew_years]
    u_r = [uk_renew[y] for y in renew_years]

    ax.plot(renew_years, c_r, color=CHINA_RED, lw=3, marker='o', markersize=4,
            label='China', zorder=5)
    ax.fill_between(renew_years, c_r, alpha=0.15, color=CHINA_RED)

    ax.plot(renew_years, g_r, color=GER_GREEN, lw=2.5, marker='s', markersize=3.5,
            label='Germany', zorder=4)
    ax.fill_between(renew_years, g_r, alpha=0.12, color=GER_GREEN)

    ax.plot(renew_years, u_r, color=WEST_LIGHT, lw=2, ls='--', marker='^',
            markersize=3.5, label='United Kingdom', zorder=3)

    ax.annotate('China: 34% → 13%\n(Headed backwards)',
                xy=(renew_years[-1], c_r[-1]), xytext=(2005, 28),
                color=CHINA_RED, fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=CHINA_RED, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=CHINA_RED, alpha=0.9))

    ax.annotate('Germany: 2% → 16%\n(Genuine transition)',
                xy=(renew_years[-1], g_r[-1]), xytext=(2002, 5),
                color='#2E8B57', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='#2E8B57', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='#2E8B57', alpha=0.9))

    ax.set_xlim(min(renew_years) - 0.5, max(renew_years) + 0.5)
    ax.set_ylim(0, 42)
    ax.set_xlabel('Year', color='#2C3E50', fontsize=11)
    ax.set_ylabel('Renewable energy (% of total final consumption)',
                  color='#2C3E50', fontsize=10)
    ax.set_title("While Europe Invests in Clean Energy,\n"
                 "China's Renewables Share Has Plummeted",
                 color='#1A1A2E', fontsize=14, fontweight='bold', pad=14)
    ax.tick_params(colors='#2C3E50', labelsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax.legend(loc='upper right', facecolor='white', edgecolor='#D9E2EC',
              labelcolor='#2C3E50', fontsize=10)

    fig.text(0.5, 0.01,
             "Source: World Bank — Renewable energy consumption "
             "(% of total final energy use).",
             ha='center', color='#666', fontsize=8.5, style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('images/viz2_renewables.png', dpi=DPI, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print('Saved viz2_renewables.png')


# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 3 — An American Pollutes Twice as Much as a Chinese Person
# ═══════════════════════════════════════════════════════════════════════════════
def viz3_per_capita():
    fig, ax = plt.subplots(figsize=(9, 6.5), facecolor=BG)
    ax.set_facecolor(BG)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#D9E2EC')
    ax.spines['bottom'].set_color('#D9E2EC')

    cap_data = {
        'United\nStates': usa_cap.get(2018, 0),
        'Canada':         can_cap.get(2018, 0),
        'Australia':      aus_cap.get(2018, 0),
        'Germany':        ger_cap.get(2018, 0),
        'United\nKingdom':uk_cap.get(2018, 0),
        'China':          china_cap.get(2018, 0),
        'India':          ind_cap.get(2018, 0),
    }

    labels = list(cap_data.keys())
    values = list(cap_data.values())
    sorted_pairs = sorted(zip(values, labels), reverse=True)
    values, labels = zip(*sorted_pairs)

    colors = []
    for lab in labels:
        if 'China' in lab:
            colors.append(CHINA_RED)
        elif 'India' in lab:
            colors.append(ACCENT_GOLD)
        else:
            colors.append(WEST_BLUE)

    bars = ax.barh(labels, values, color=colors, height=0.6,
                   edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}t', va='center', ha='left', fontsize=10.5,
                fontweight='bold' if val > 12 else 'normal', color='#1A1A2E')

    us_val = cap_data['United\nStates']
    cn_val = cap_data['China']
    ratio = us_val / cn_val

    ax.axvline(cn_val, color=CHINA_RED, lw=1.5, ls=':', alpha=0.7)

    us_idx = list(labels).index('United\nStates')
    # Place the annotation below the US bar (in inverted-y space, that's a higher numerical y)
    ax.annotate(f'The average American\nemits {ratio:.1f}× more CO₂\nthan the average Chinese',
                xy=(us_val, us_idx), xytext=(11.5, us_idx + 1.5),
                color=WEST_BLUE, fontsize=10.5, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=WEST_BLUE, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.4', facecolor=PANEL_LIGHT,
                          edgecolor=WEST_BLUE))

    ax.set_xlabel('CO₂ emissions per person (metric tonnes, 2018)',
                  color='#35566E', fontsize=11)
    ax.set_title('An American Pollutes Twice as Much\n'
                 'as a Chinese Person — Every Single Year',
                 color='#1A1A2E', fontsize=14, fontweight='bold', pad=14)
    ax.tick_params(colors='#4C6B82', labelsize=10)
    ax.set_xlim(0, 22)
    ax.invert_yaxis()  # largest at top reads more naturally

    west_patch  = mpatches.Patch(color=WEST_BLUE, label='Western nations')
    china_patch = mpatches.Patch(color=CHINA_RED, label='China')
    india_patch = mpatches.Patch(color=ACCENT_GOLD, label='India')
    ax.legend(handles=[west_patch, china_patch, india_patch],
              loc='lower right', fontsize=10, framealpha=1,
              facecolor='#F4FBFF', edgecolor='#9CBED6', labelcolor='#12324A')

    fig.text(0.5, 0.01,
             'Per-capita framing: every human deserves equal rights to the atmosphere.  '
             'Source: World Bank, 2018.',
             ha='center', color='#5F7D95', fontsize=8.5, style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('images/viz3_per_capita.png', dpi=DPI, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print('Saved viz3_per_capita.png')


# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 4 — The West Built the CO₂ Already in Our Atmosphere
# ═══════════════════════════════════════════════════════════════════════════════
def viz4_cumulative():
    fig, ax = plt.subplots(figsize=(9, 6.5), facecolor=BG)
    ax.set_facecolor(BG)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#D9E2EC')
    ax.spines['bottom'].set_color('#D9E2EC')

    cum_years = range(1960, 2019)

    def cumulative(series, years):
        return sum((series.get(y, 0) or 0) for y in years)

    cum_usa   = cumulative(usa_kt, cum_years)
    cum_china = cumulative(china_kt, cum_years)
    cum_ger   = cumulative(ger_kt, cum_years)
    cum_uk    = cumulative(uk_kt, cum_years)
    cum_fra   = cumulative(fra_kt, cum_years)
    cum_can   = cumulative(can_kt, cum_years)
    cum_jpn   = cumulative(jpn_kt, cum_years)

    west_cum = cum_usa + cum_ger + cum_uk + cum_fra + cum_can + cum_jpn
    scale = 1e6

    cat_labels = ['United States\nalone', '"The West"\n(US+EU+CA+JP)', 'China']
    cat_values = [cum_usa / scale, west_cum / scale, cum_china / scale]
    cat_colors = [WEST_BLUE, WEST_DARK, CHINA_RED]
    cat_hatch = ['', '///', '']

    bars = ax.bar(cat_labels, cat_values, color=cat_colors, width=0.5,
                  edgecolor='white', linewidth=1.5)
    for bar, h in zip(bars, cat_hatch):
        bar.set_hatch(h)

    for i, (bar, val) in enumerate(zip(bars, cat_values)):
        offset = 14 if i != 1 else 18
        ax.text(bar.get_x() + bar.get_width() / 2, val + offset,
                f'{val:.0f}B\ntonnes', ha='center', va='bottom',
                fontsize=12, fontweight='bold', color='#1A1A2E')

    ratio = west_cum / cum_china
    ax.annotate(f'The West emitted\n{ratio:.1f}× more CO₂\nthan China\nsince 1960',
                xy=(1, west_cum / scale), xytext=(1.45, 470),
                ha='left', va='center',
                color=WEST_DARK, fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=WEST_DARK, lw=1.4),
                bbox=dict(boxstyle='round,pad=0.35', facecolor=PANEL_LIGHT,
                          edgecolor=WEST_DARK))

    ax.set_ylabel('Cumulative CO₂ emissions, 1960–2018 (billion metric tonnes)',
                  color='#35566E', fontsize=10)
    ax.set_title("The West Built the CO₂ Already in\n"
                 "Our Atmosphere — China Is Just Catching Up",
                 color='#1A1A2E', fontsize=14, fontweight='bold', pad=14)
    ax.tick_params(colors='#4C6B82', labelsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}B'))
    ax.set_ylim(0, 540)

    fig.text(0.5, 0.01,
             'Cumulative emissions since 1960 show who actually filled the atmosphere with CO₂.  '
             'Source: World Bank.',
             ha='center', color='#5F7D95', fontsize=8.5, style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('images/viz4_cumulative.png', dpi=DPI, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print('Saved viz4_cumulative.png')


# Print the actual numbers we got so they can be cited in HTML.
def print_summary():
    years = range(1990, 2019)
    west_total_2018 = sum(s.get(2018, 0) for s in [usa_kt, ger_kt, uk_kt, fra_kt, can_kt, jpn_kt])
    west_total_1990 = sum(s.get(1990, 0) for s in [usa_kt, ger_kt, uk_kt, fra_kt, can_kt, jpn_kt])
    print(f"China 1990 emissions: {china_kt.get(1990, 0)/1e6:.2f}B tonnes")
    print(f"China 2018 emissions: {china_kt.get(2018, 0)/1e6:.2f}B tonnes")
    print(f"China change:        +{(china_kt.get(2018, 0) - china_kt.get(1990, 0))/1e6:.2f}B tonnes")
    print(f"West 1990 emissions:  {west_total_1990/1e6:.2f}B tonnes")
    print(f"West 2018 emissions:  {west_total_2018/1e6:.2f}B tonnes")
    print(f"West change:          {(west_total_2018 - west_total_1990)/1e6:+.2f}B tonnes")
    print(f"China renew 1990: {china_renew.get(1990, 0):.1f}%")
    print(f"China renew 2018: {china_renew.get(2018, 0):.1f}%")
    print(f"Ger renew 1990: {ger_renew.get(1990, 0):.1f}%")
    print(f"Ger renew 2018: {ger_renew.get(2018, 0):.1f}%")
    print(f"USA 2018 per capita: {usa_cap.get(2018, 0):.2f}")
    print(f"China 2018 per capita: {china_cap.get(2018, 0):.2f}")

    cum_years = range(1960, 2019)
    cum_usa   = sum((usa_kt.get(y, 0) or 0)   for y in cum_years) / 1e6
    cum_china = sum((china_kt.get(y, 0) or 0) for y in cum_years) / 1e6
    west_cum  = sum((sum((s.get(y, 0) or 0) for s in [usa_kt, ger_kt, uk_kt, fra_kt, can_kt, jpn_kt]))
                    for y in cum_years) / 1e6
    print(f"Cumulative USA:   {cum_usa:.0f}B tonnes")
    print(f"Cumulative West:  {west_cum:.0f}B tonnes")
    print(f"Cumulative China: {cum_china:.0f}B tonnes")
    print(f"West/China ratio: {west_cum/cum_china:.2f}")


if __name__ == '__main__':
    viz1_china_vs_west_emissions()
    viz2_renewables()
    viz3_per_capita()
    viz4_cumulative()
    print()
    print_summary()
