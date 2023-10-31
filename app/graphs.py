# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker


'''
properties
'''

colors_ms = {   
    'blue': [69, 114, 167], 
    'red': [170, 70, 67],   
    'green': [137, 165, 78],
    'purple': [113, 88, 143],        
    'cyan': [65, 152, 175],
    'orange': [219, 132, 61], 
}

colors_pbs = {   
    'orange': [252, 127, 40], 
    'blue': [39, 120, 178],   
    'green': [51, 159, 52],
}

use = colors_pbs
colors_list = [
    use['orange'],
    use['blue'],
    use['green'],
]


'''
functions
'''

#inputf can be a path to csv file or pandas dataframe
#columns can have any names but ...
#data in first column must be channels, data in second must be views  
def pie_chart(inputf, outputf, title_text, include_others=True):  

    if isinstance(inputf, str): df = pd.read_csv(inputf)
    elif isinstance(inputf, pd.DataFrame): df = inputf 
    #print('\n', df.head())  
    
    #keep and rename first two columns    
    df = df[df.columns[[0,1]]]
    df.columns = ['Channel', 'Views']       
    
    #split into top 5 and others
    cut = 5 if include_others else 6
    df_others = df.iloc[cut:]
    df = df.iloc[:cut]
    print('\n', df)   
    
    #add others
    if include_others:
        df['Channel'] = df['Channel'].apply(lambda x: x.replace(' - Masterpiece', ''))
        others = df_others.sum()
        others['Channel'] = 'Others'
        df = df.append(others, ignore_index=True) 
    
    #convert colors into mpl form
    alpha = 0.8
    alpha = 1.0
    colors = []
    for x in colors_ms.values():
        color = []
        for y in x:
            y = float(y) / 255
            color.append(y)
        color = tuple(color + [alpha])  
        colors.append(color)
    
    
    '''
    plot
    '''
    
    #callback for autopct
    def show_autopct(x):
        return ('%1.f%%' % x) if x > 2 else '' 
    
    fig, ax = plt.subplots(1, figsize=(7, 7))
    
    patches, texts, autotexts = ax.pie(        
        df['Views'],
        labels = df['Channel'], 
        colors = colors,
        explode = (0.15, 0.15, 0.15, 0.15, 0.15, 0.15),
        shadow = False,
        startangle = 90,
        autopct = show_autopct,
        pctdistance=0.85
    )
    
    plt.axis('equal')
    plt.gca().set_aspect('equal', adjustable='box')
    title = fig.suptitle(title_text, color='#777777', size=20)   
    
    
    '''
    styles
    '''
    count = 0
    for patch in patches:
        patch.set_edgecolor('#cccccc')
        patch.set_linewidth(2)
        patch.set_facecolor(colors[count])
        count += 1
  
    for text in texts:
        text.set_color('#666666') 
        text.set_size(13.5)
    
    for text in autotexts:
        text.set_color('white') 
        text.set_size(11)
        text.set_weight('bold')
        
        
    '''
    save and show
    '''
    
    plt.savefig(outputf, dpi=72, bbox_inches='tight')
    plt.show()
    
    
def timeline(inputf, outputf, title_text, to_plot=5):

    if isinstance(inputf, str): df = pd.read_csv(inputf)
    elif isinstance(inputf, pd.DataFrame): df = inputf 
    print('\n', df)
    
    text_color = '#666666'
    alpha = 0.4  
    x_ticks = range(0, len(df.index))
    
    #plot
    fig, ax = plt.subplots(1, figsize=(9,4))
    #df = df[df.columns[::-1]] #reverse order of columns
    print(df.columns)
    patches = []
    
    count = 0
    for col, color in zip(df.columns, colors_ms): 
        count += 1
        if count > to_plot: break
        
        #plot lines
        plot = ax.plot(x_ticks, df[col], 
                linewidth=4, marker='o', markersize=4, alpha=alpha)            
        #get line color
        color = plot[0].get_color() 
        
        #add fill
        ax.fill_between(x_ticks, df[col], 0,
                 facecolor=color,
                 alpha=0.00) 
        
        #add legend items         
        patches.append(mpatches.Patch(color=color, alpha=alpha+0.1, label=col))         
    
    #add margins around canvas
    plt.margins(0.03, 0.065)  
    
    #set x labels
    plt.xticks(x_ticks, df.index.values)
    
    #add title 
    title_margin = 1.11 + len(patches) * 0.07
    print('\n', title_margin) 
    title = fig.suptitle(title_text, color=text_color, size=20, x=0.5, y=title_margin)
    
    
    '''
    create legend
    '''
  
    text_color_leg = '#444444'    
    
    #patches = patches[::-1] #reverse back order of patches (column labels)
    legend = plt.legend(handles=patches, loc=(0, 1), fontsize=13.5, frameon=False)

    for text in legend.get_texts():
        plt.setp(text, color=text_color_leg)    
    

    '''
    more graph styles
    '''

    #set formatting for x and y labels
    text_color = '#666666'

    #remove all tick parameters, lighten colors, and make text smaller
    ax.tick_params(top='off', right='off', bottom='off', left='off', 
                    colors=text_color, labelsize=13.5, which='both')
    ax.tick_params(axis='y', labelsize=13.5, which='both')
    
    #highlight saturday and sunday for easier reading
    for xtick in ax.get_xticklabels():
        if xtick.get_text() == 'Sun' or xtick.get_text() == 'Sat':
            xtick.set_color('#dd0000')


    #lighten frame
    for spine in ax.spines.values():
        spine.set_color('none')
        spine.set_linewidth(0.3)
     
    #remove first y label tick
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].set_visible(False) 
     
    #adjust padding to major y ticks and x ticks 
    #ax.tick_params(axis='y', which='major', pad=12)
    #ax.tick_params(axis='x', which='major', pad=12)
    
    ax.xaxis.labelpad = 0
    
         
    '''
    save and show
    '''
    
    plt.tight_layout()
    plt.savefig(outputf, dpi=72,
                bbox_inches='tight', bbox_extra_artist=[title])
    plt.show()
    
    
def one_bar_horiz(folder, img_name, title_text, y_labels, x_data, y_data,
                  bar_labels=False, bar_labels_inside=True, titlesize=18, labelsize=13):

    #set formatting for x and y labels
    text_color = '#666666'
    #height = 0.8
    
    #plot
    fig, ax = plt.subplots(1, figsize=(10, 5))    
    bars = ax.barh(y_data, x_data, align='center', color='#4682b4', edgecolor='none')    
    ax.set_title(title_text, color='#777777', size=titlesize, y=1.07)

    #add y_labels
    ax.set_yticklabels(y_labels)
   
    #set y_labels padding
    ax.set(yticks=range(len(y_data)), ylim=[-1, len(y_data)])
    ax.tick_params(axis='y', which='major', pad=11)

    #format major x ticks 
    ax.tick_params(axis='x', which='major', pad=5)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
   
    #remove all tick parameters, lighten colors, and make text smaller
    ax.tick_params(top='off', right='off', bottom='off', left='off', 
                    colors=text_color, labelsize=labelsize, which='both')
    ax.tick_params(axis='y', labelsize=labelsize, which='both')    
                    
    #lighten frame
    for spine in ax.spines.values():
        spine.set_color('none')
        spine.set_linewidth(0.3)

    #remove first and last x label ticks
    xticks1 = ax.xaxis.get_major_ticks()
    xticks1[0].set_visible(False)   
    xticks1[-1].set_visible(False)    

    #optional: move x labels to bars 
    if bar_labels:   
        #drop x labels    
        for xtick in ax.xaxis.get_major_ticks():
            xtick.set_visible(False)
        
        #add values to bars
        #ax.text(x_loc, y_loc, value)
        for bar in bars:
            ax.text(
                bar.get_width() - labelsize/3, 
                bar.get_y() + bar.get_height()/2,                
                str(int(bar.get_width())), 
                va='center', color='w', fontsize=labelsize, fontweight='bold'
                )

    plt.axis('tight')
    fig.tight_layout()
    fig.savefig(folder + '/' + img_name, dpi=100)
    plt.show()
    

def one_bar_horiz_3_stack(folder, img_name, title_text, y_labels, x_data, y_data):

    #set formatting for x and y labels
    text_color = '#666666'
    height = 0.75
    
    #convert colors into mpl form
    alpha = 0.85
    colors = []
    for x in colors_list:
        color = []
        for y in x:
            y = float(y) / 255
            color.append(y)
        color = tuple(color + [alpha])  
        colors.append(color)
    
    #plot
    fig, ax = plt.subplots(1, figsize=(10, 5))  
    
    left = 0
    patches = []     
    for column, color in zip(x_data, colors):
        ax.barh(y_data, x_data[column], align='center', color=color, edgecolor='none', left=left, height=height)
        left += x_data[column]
        
        leg_title = column.upper() if column == 'ott' else column.title() 
        patch = mpatches.Patch(color=color, alpha=alpha, label=leg_title)
        patches.append(patch)
        
    legend = plt.legend(handles=patches, 
               loc=(0.75, 0.25), fontsize=13.5, frameon=False) #x loc first, then y

    for text in legend.get_texts():
        plt.setp(text, color='#666666') 
        
    plt.axis('tight')        
    
    ax.set_title(title_text, color='#777777', size=18, y=1.00)

    #add y_labels
    ax.set_yticklabels(y_labels)
    
    #set y_labels padding
    ax.set(yticks=range(len(y_data)), ylim=[-1, len(y_data)])
    ax.tick_params(axis='y', which='major', pad=11)

    #format major x ticks 
    ax.tick_params(axis='x', which='major', pad=-10)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
   
    #remove all tick parameters, lighten colors, and make text smaller
    ax.tick_params(top='off', right='off', bottom='off', left='off', 
                    colors=text_color, labelsize=13, which='both')                    
    ax.tick_params(axis='y', labelsize=13, which='both')    
                    
    #lighten frame
    for spine in ax.spines.values():
        spine.set_color('none')
        spine.set_linewidth(0.3)

    #remove first and last x label ticks
    xticks1 = ax.xaxis.get_major_ticks()
    xticks1[0].set_visible(False)   
    xticks1[-1].set_visible(False)     

    plt.axis('tight')
    fig.tight_layout()
    fig.savefig(folder + '/' + img_name, dpi=100)
    plt.show() 
    