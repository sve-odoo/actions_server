obj = self.pool.get('product.product')
ids = obj.search(cr,uid,[],context=context)
obj.write(cr,uid,ids,{},context=context)