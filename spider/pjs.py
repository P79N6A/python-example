import execjs
print execjs.eval("'red yellow blue'.split(' ')")

ctx = execjs.compile("""
     function add(x, y) {
         return x + y;
     }
     function minus(x,y){
         return x-y;
     }
 """)
print ctx.call("add", 1, 2)
print ctx.call("minus", 1, 2)
