class  LOGS{
    static 变量查看(变量名,变量){
        console.log('--------------')
        console.log('变量名：' + 变量名)
        console.log(变量)
        console.log('类型：' + typeof(变量))
        try{
            console.log('大小: ' + 变量.length)

        }catch (TypeError){
            console.log('大小: 不支持显示')
        }
        console.log('----------------')
    }
}