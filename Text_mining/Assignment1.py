def date_sorter():
    #df.str.extract(r'(\d?\d)/(\d?\d)/(\d{2,4})')
    #df.str.extract(r'([1,2]\d\d\d)')
    #for i in df :
    #    if i.find(r' ?(Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)[a-z]* ?'):
    #        print(i)
    #df[501] = " March AprJun "
    #df[501].contains(r'(Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)[a-z]*')
    pd.set_option('display.max_rows', 1000)
    #df.str.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z,]* (?:\d{2,4}(?:,)?)? ?(?:\d{2,4})?')

    #df.str.findall(r'(?:\d{1,2} )?(?:Jan|Feb|(?:Mar[^kir])|Apr|May|Jun|(?:Jul[^i])|Aug|Sep|Oct|Nov|(?:Dec[e ]))[a-z., ]*(?:\d{2,4}(?:,)?)? ?(?:\d{2,4})?|(?:\d?\d)?[/](?:\d?\d?)[/](?:\d{2,4})|(?:\d?\d)?[-](?:\d?\d)[-](?:\d{2,4})|(?:\d?)?/(?:\d{2,4})|(?:[1,2]\d\d\d)')

    df.str.findall(r'(?:\d{1,2} )?(?:Jan|Feb|(?:Mar[^kir])|Apr|May|Jun|(?:Jul[^i])|Aug|Sep|Oct|Nov|(?:Dec[e ]))[a-z., ]*(?:\d{2,4}(?:,)?)? ?(?:\d{2,4})?|(?:\d?\d)?[/](?:\d?\d?)[/](?:\d{2,4})|(?:\d?\d)?[-](?:\d?\d)[-](?:\d{2,4})|(?:\d?)?/(?:\d{2,4})|(?:[1,2]\d\d\d)')



    #04/20/2009; 04/20/09; 4/20/09; 4/3/09
    a = df.str.extractall(r'(\d?\d)?[/](\d?\d?)[/](\d{2,4})')
    a.reset_index(inplace=True)
    a.columns=['index','match','month','day','year']
    a['year']=a['year'].apply(lambda x: '19'+x if len(x)<=2 else x)
    #print(a)
    b = df.str.extractall(r'(\d?\d)?[-](\d?\d)[-](\d{2,4})')
    b.reset_index(inplace=True)
    b.columns=['index','match','month','day','year']
    b['year']=b['year'].apply(lambda x: '19'+x if len(x)<=2 else x)

    #print(b)

    #just year
    c = df.str.extractall(r'([1,2]\d\d\d)')
    c.reset_index(inplace=True)
    c.columns=['index','match','year']
    for i in c['year']:
        if "," in i : c = c[c['year'] != i]
    c['month'] = 1
    c['day'] = 1

    #print(c)

    d = df.str.extractall(r'(\d{1,2} )?(Jan|Feb|Mar[^kir]|Apr|May|Jun|Jul[^i]|Aug|Sep|Oct|Nov|Dec[e ])[a-z., ]*(\d{2,4})?[, ]?(?:\d{2,4})?')
    d.reset_index(inplace=True)
    d.columns=['index','match','day','month','year']
    import numpy as np


    f = df.str.extractall(r'(Jan|Feb|Mar[^kir]|Apr|May|Jun|Jul[^i]|Aug|Sep|Oct|Nov|Dec[e ])[a-z., ]*((?:\d{1,2})[, ]*)?(\d{4})?')
    f.reset_index(inplace=True)
    f.columns=['index','match','month','day','year']

    f = f[f.year.notnull()]
    f['day'] = f['day'].apply(lambda x: x.replace(',',''))
    #print(" df f")
    #print(f)
    #print(" df d",d)
    # on retire les indices presents dans d qui sont aussi dans f
    for i in d['index'].values:
        if  i in f['index'].values :
            d=d[d['index'] != i]

    d = d[d.year.notnull()]
    d['day']=d['day'].apply(lambda x: 1 if type(x) != str else x)
    save=[]
    for i in c['index'].values :
        if ((i in a['index'].values) or (i in b['index'].values) or (i in d['index'].values) or (i in f['index'].values)):
            c=c[c['index'] != i]
    #print(c)


    f['month'] = f.month.apply(lambda x: x[:3])
    f['month'] = pd.to_datetime(f.month, format='%b').dt.month
    d['month'] = d.month.apply(lambda x: x[:3])
    d['month'] = pd.to_datetime(d.month, format='%b').dt.month
    final = pd.concat([a,b,c,d,f])
    for i in final.year:
        if len(i) <4:
            final=final[final['year'] != i]
    final['year'] = final['year'].apply(lambda x: x.replace(',',''))
    months = ["Januar","Februar","March","April","May","June","July","August","Septemb","October","November","Decemb"]

    final['date'] =pd.to_datetime(final['month'].apply(str)+'/'+final['day'].apply(str)+'/'+final['year'].apply(str))
    final = final.sort_values(by='index').set_index('index')
    #print(final)           

    myList = final['date']
    answer = pd.Series([i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])],np.arange(500))
    #print(answer)
    #for i in range(len(s)):
    #    print(i,  s[i])
    return answer, final
answer,final = date_sorter()
for i in range(len(df)):
    print(final["date"][i],df[i])