# Coloque a planilha original do desafio nesta pasta como base_original.xlsx e rode: python tratamento.py
import pandas as pd, json
df=pd.read_excel('base_original.xlsx',dtype=str)
st={'Delivered':'Entregue','Cancelled':'Cancelada'}
out=pd.DataFrame({
 'id':df.sale_id.astype(int),
 'data':df.SaleDateSanitized.where(df.SaleDateSanitized!='INVALID'),
 'modelo':df.PorscheModelSanitized,
 'linha':df.PorscheModelSanitized.str.split().str[0],
 'ano':df.ModelYearSanitized.astype(int),
 'preco':df.SalesPriceSanitized.astype(float),
 'km_milhas':df.VehicleMileageSanitized.astype(int),
 'pagamento':df.PayMethodSanitized,
 'cidade':df.CitySanitized,'estado':df.StateSanitized,
 'status_original':df.DeliveryStatusSanitized,
 'status':df.DeliveryStatusSanitized.map(lambda s: st.get(s,'Em andamento')),
})
out.to_csv('base_tratada.csv',index=False,encoding='utf-8')
out.to_excel('base_tratada.xlsx',index=False)
rows=[[r.id,r.modelo,r.linha,int(r.ano),float(r.preco),r.pagamento,r.cidade,r.estado,r.status,r.status_original] for r in out.itertuples()]
json.dump(rows,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
print(out.preco.sum(), out.preco.mean(), out.groupby('linha').preco.sum().sort_values(ascending=False).to_dict())
print(out.groupby('pagamento').preco.agg(['sum','count','mean']).sort_values('sum',ascending=False))
print(out.groupby('estado').preco.sum().sort_values(ascending=False).head(6).to_dict(), out.status.value_counts().to_dict())
