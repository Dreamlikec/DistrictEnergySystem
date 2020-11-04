<template>
    <div>
    <div class="legend_container">
        <ul>
            <li v-for="item in legendData">
                <button class="btn-link btn-legend-item" @click="changeLegrend(item,$event)"><span class="legend-item-bg" :style="'background-color:'+legendColor[item]"></span>{{item}}</button>
            </li>
        </ul>
    </div>
    <div id="myLine" :style="{width:'100%',height:'300px'}"></div>
    </div>
</template>
<script type="ecmascript-6">
import {getPhyLogiLoadApi} from '@/apis'
export default {
    data(){
        return {
            xData:[],
            series:[],
            legendData:[],
            legendColor:{},
            storage:{},
            colors:['#5793f3', '#d14a61', '#675bba']
        }
    },
    methods:{
        drawLine(){
            let myLine = this.$echarts.init(document.getElementById('myLine'));
            let option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    selectedMode:'single'
                },
                grid: {
                    left: '3%',
                    right: '7%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {
                            alignWithLabel: true
                        },
                        data: this.xData,
                        name: '快照时间'
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '统计值'
                    }
                ],
                series: this.series
            };
            myLine.setOption(option);
            window.addEventListener("resize", () => { myLine.resize();});
        },
        fetchData(){
            getPhyLogiLoadApi(this.$store.state.inspection.reportInfo.batch_id).then((res) => {
                if(res.status === 200){
                    let _dataArray = res.data,
                        len = _dataArray.length;
                    for(let i=0;i<len;i++){
                        if(!this.legendData.includes(_dataArray[i].instance_name)){
                            this.legendColor[_dataArray[i].instance_name] = this.colors[this.legendData.length];
                            this.legendData.push(_dataArray[i].instance_name);
                        }
                        let _obj = {
                            name:_dataArray[i].stat_name,
                            type:'line',
                            smooth:true,
                            dbname:_dataArray[i].instance_name,
                            color:this.legendColor[_dataArray[i].instance_name],
                            data:_dataArray[i].stat_value.split(',')
                        }
                        this.series.push(_obj)
                    }
                    this.xData = _dataArray[0].snap_time.split(',')
                    this.drawLine();
                }
            })
        },
        changeLegrend(item,e){
            let _obj = {},
                len = this.series.length,
                _data = this.series;
            let thisDom = e.currentTarget;
            thisDom.classList.toggle('btn-selected');
            for(let i = 0; i < len; i++){
                if(item === _data[i].dbname){
                    //如果为空，说明被选，置为存储的数据
                    if(_data[i].data.length === 0){
                        _data[i].data = this.storage[item][_data[i].name]
                    }else{
                        //先存数据，再置为空
                        _obj[_data[i].name] = _data[i].data;
                        _data[i].data = []
                    }
                }
            }
            //存储数据
            this.storage[item] = _obj;
            this.drawLine();
        }
    },
    mounted(){
        this.fetchData();
    }
}
</script>
<style scoped lang="stylus" rel="stylesheet">
.legend_container{
    text-align center
    li {
        list-style none
        display inline
    }
}
.btn-link, .btn-link:active, .btn-link:focus, .btn-link:hover {
    border-color: transparent;
    background-color: transparent;
    box-shadow: none;
}
.btn-legend-item {
    color: rgb(72, 72, 72);
    padding: 0px;
}
.legend-item-bg {
    display:inline-block;
    width: 20px;
    height: 12px;
    margin-right: 5px;
    border-radius: 2px;
}
.btn-selected{
    opacity 0.3
}
</style>