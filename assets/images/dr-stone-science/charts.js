/**
 * Dr. Stone Science Guide - ECharts Configuration
 * Chart logic for arc distribution and field distribution charts
 */
(function() {
  'use strict';

  // Common dark theme colors
  var COLORS = ['#00d4aa', '#ff6b35', '#6495ed', '#ffc107', '#90ee90', '#da70d6', '#ffa500', '#ff6b9d'];

  // Chart 1: Arc invention count distribution (bar chart)
  var chartArcs = document.getElementById('chart-arcs');
  if (chartArcs && typeof echarts !== 'undefined') {
    var arcsChart = echarts.init(chartArcs, null, { renderer: 'canvas' });
    var arcsOption = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        textStyle: { color: '#e8ecf1', fontFamily: 'sans-serif' },
        backgroundColor: '#141b2d',
        borderColor: '#2a3450',
        borderWidth: 1
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '8%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: [
          '序章篇',
          '科学王国篇',
          '石之战争篇',
          '大航海时代篇',
          '宝岛篇',
          '新世界篇',
          '石至太空篇'
        ],
        axisLabel: {
          color: '#8892a4',
          fontSize: 11,
          rotate: 30
        },
        axisLine: { lineStyle: { color: '#2a3450' } }
      },
      yAxis: {
        type: 'value',
        name: '发明数量',
        nameTextStyle: { color: '#8892a4' },
        axisLabel: { color: '#8892a4' },
        splitLine: { lineStyle: { color: '#2a3450', type: 'dashed' } },
        axisLine: { lineStyle: { color: '#2a3450' } }
      },
      series: [{
        name: '发明数量',
        type: 'bar',
        barWidth: '50%',
        data: [7, 8, 8, 7, 6, 7, 7],
        itemStyle: {
          color: function(params) {
            var colorList = [
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#00d4aa' },
                { offset: 1, color: '#008f72' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#00d4aa' },
                { offset: 1, color: '#008f72' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#ff6b35' },
                { offset: 1, color: '#cc5529' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#6495ed' },
                { offset: 1, color: '#4a6fbd' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#da70d6' },
                { offset: 1, color: '#a854a5' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#ffc107' },
                { offset: 1, color: '#cc9a06' }
              ]),
              new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#ffa500' },
                { offset: 1, color: '#cc8400' }
              ])
            ];
            return colorList[params.dataIndex % colorList.length];
          },
          borderRadius: [4, 4, 0, 0]
        },
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 212, 170, 0.3)' }
        },
        label: {
          show: true,
          position: 'top',
          color: '#e8ecf1',
          fontSize: 12,
          fontWeight: 'bold'
        }
      }]
    };
    arcsChart.setOption(arcsOption);
    window.addEventListener('resize', function() { arcsChart.resize(); });
  }

  // Chart 2: Science field distribution (pie chart)
  var chartFields = document.getElementById('chart-fields');
  if (chartFields && typeof echarts !== 'undefined') {
    var fieldsChart = echarts.init(chartFields, null, { renderer: 'canvas' });
    var fieldsOption = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        textStyle: { color: '#e8ecf1', fontFamily: 'sans-serif' },
        backgroundColor: '#141b2d',
        borderColor: '#2a3450',
        borderWidth: 1,
        formatter: '{b}: {c}项 ({d}%)'
      },
      legend: {
        orient: 'horizontal',
        bottom: '0%',
        textStyle: { color: '#8892a4', fontSize: 12 },
        itemGap: 16
      },
      series: [{
        name: '科学领域',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderColor: '#0a0e17',
          borderWidth: 2,
          borderRadius: 6
        },
        label: {
          show: true,
          color: '#e8ecf1',
          fontSize: 12,
          formatter: '{b}\n{d}%'
        },
        emphasis: {
          label: { show: true, fontSize: 14, fontWeight: 'bold' },
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 212, 170, 0.4)' }
        },
        labelLine: {
          lineStyle: { color: '#2a3450' }
        },
        data: [
          { value: 18, name: '化学', itemStyle: { color: '#00d4aa' } },
          { value: 14, name: '工程学', itemStyle: { color: '#ffc107' } },
          { value: 12, name: '物理学', itemStyle: { color: '#6495ed' } },
          { value: 8, name: '生物学', itemStyle: { color: '#90ee90' } },
          { value: 4, name: '数学', itemStyle: { color: '#da70d6' } },
          { value: 4, name: '天文学', itemStyle: { color: '#ffa500' } }
        ]
      }]
    };
    fieldsChart.setOption(fieldsOption);
    window.addEventListener('resize', function() { fieldsChart.resize(); });
  }
})();
