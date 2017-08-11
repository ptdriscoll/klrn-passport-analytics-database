# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


'''
properties
'''

colors_ms = {   
    'blue': [69, 114, 167], 
    'red': [170, 70, 67],   
    'green': [137, 165, 78],
    'purple': [113, 88, 143],
    'cyan': [65, 152, 175],
    'orange': [219, 132, 61] 
}


'''
functions
'''

#inputf can be a path to csv file or pandas dataframe
#columns can have any names but ...
#data in first column must channels, data in second must be views  
def pie_chart(inputf, outputf, title_text, include_others=True):  

    if isinstance(inputf, str): df = pd.read_csv(inputf)
    elif isinstance(inputf, pd.DataFrame): df = inputf 
    #print '\n',df.head()  
    
    #keep and rename first two columns    
    df = df[df.columns[[0,1]]]
    df.columns = ['Channel', 'Views']       
    
    #split into top 5 and others
    cut = 5 if include_others else 6
    df_others = df.iloc[cut:]
    df = df.iloc[:cut]
    print '\n', df   
    
    #add others
    if include_others:
        df['Channel'] = df['Channel'].apply(lambda x: x.replace(' - Masterpiece', ''))
        others = df_others.sum()
        others['Channel'] = 'Others'
        df = df.append(others, ignore_index=True) 
        #print '\n', df
        #print '\n', others, '\n'
    
    #convert colors into mpl form
    alpha = 0.8
    alpha = 1.0
    colors = []
    for x in colors_ms.itervalues():
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
        return ('%1.f%%' % x) if x > 5 else '' 
    
    fig, ax = plt.subplots(1, figsize=(4, 4))
    
    patches, texts, autotexts = ax.pie(        
        df['Views'],
        labels = df['Channel'], 
        colors = colors,
        explode = (0.15, 0.15, 0.15, 0.15, 0.15, 0.15),
        shadow = False,
        startangle = 60,
        autopct = show_autopct,

    )
    
    plt.axis('tight')
    title = fig.suptitle(title_text, color='#777777', size=20, y=1.15)
    
    
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
    
    plt.tight_layout()
    plt.savefig(outputf, dpi=72,
                bbox_inches='tight', bbox_extra_artist=[title])
    plt.show()
    
    
def timeline(inputf, outputf, title_text, to_plot=5):

    if isinstance(inputf, str): df = pd.read_csv(inputf)
    elif isinstance(inputf, pd.DataFrame): df = inputf 
    print '\n',df
    
    text_color = '#666666'
    alpha = 0.4  
    x_ticks = range(0, len(df.index))
    
    #plot
    fig, ax = plt.subplots(1, figsize=(9,4))
    #df = df[df.columns[::-1]] #reverse order of columns
    print df.columns
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
    print '\n', title_margin 
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