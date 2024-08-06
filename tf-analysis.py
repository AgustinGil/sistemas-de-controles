from numpy import array, insert
from sympy import limit, Symbol
from matplotlib.pyplot import plot, xlabel, ylabel, title, savefig, figure, rcParams, margins, axhline, tick_params, tight_layout, ylim, yticks 
from control import tf, step_response, step_info
from io import BytesIO

def final_value_theorem(numerator: list[float], denominator: list[float]) -> float:
    s = Symbol('s')
    sym_numerator = 0
    sym_denominator = 0 

    for i,n in enumerate(numerator):
        num = n * (s) ** (len(numerator)-i)
        sym_numerator += num

    for i,n in enumerate(denominator):
        num = n * (s) ** (len(denominator)-i)
        sym_denominator += num
    
    return limit(sym_numerator/sym_denominator,s,0)

def plot_styling() -> None:
    rcParams["font.size"] = "6"
    
    figure(figsize=(8,4))
    margins(0)
    title('Step Response')
    tight_layout()
    
    xlabel('Time (seconds)')
    ylabel('Amplitude')
    
    tick_params(axis="both",direction="in",top=True,bottom=True,left=True,right=True)

def fix_top_tick(y) -> None:    
    ticks = yticks()[0]
    ticks_diff = ticks[len(ticks) - 1] - ticks[len(ticks) - 2]
    
    for tick in ticks:
        if tick < max(y):
            last_tick = tick
        else:
            break

    tick_excess = max(y) - last_tick
    ylim(min(y),max(y) + ticks_diff - tick_excess)

def get_plot(numerator: list[float], denominator: list[float], dead_time: float = 0) -> BytesIO:
    transfer_function = tf(numerator,denominator)
    t, y = step_response(transfer_function)
    y_ss = final_value_theorem(numerator,denominator)
    
    if dead_time != 0:
        t = array([time + dead_time for time in t])        
        t = insert(t,0,0,axis=0)
        y = insert(y,0,0,axis=0)
    
    plot_styling()

    plot(t,y,color="black",linewidth=0.5)
    axhline(y=y_ss,color="black",linestyle="dashed",linewidth=0.5)
    axhline(y=y_ss+y_ss*0.05,color="gray",linestyle="dashed",linewidth=0.5)
    axhline(y=y_ss-y_ss*0.05,color="gray",linestyle="dashed",linewidth=0.5)

    fix_top_tick(y)

    fig = BytesIO()
    savefig('a.png',format='png',dpi=150)
    
    return fig.getvalue()


def get_values(numerator: list[float], denominator: list[float], dead_time: float = 0) -> dict:
    transfer_function = tf(numerator,denominator)    
    y_ss = final_value_theorem(numerator,denominator)

    step_information = step_info(transfer_function)
    step_values = {
        'FinalValue' :      "{:.4f}".format(y_ss),
        'Overshoot' :       "{:.4f}".format(step_information['Overshoot']),
        'RiseTime' :        "{:.4f}".format(step_information['RiseTime']),
        'DelayTime' :       "{:.4f}".format((y_ss * 0.5) - dead_time),
        'SettlingTime' :    "{:.4f}".format(step_information['SettlingTime'] - dead_time),
        'Poles' :           transfer_function.poles()
    }

    return step_values

#get_plot([100],[1,5,100],0.4)
#s = get_values([100],[1,5,100],0.4)
#for x in s:
#    print(f"{x} {s[x]}")