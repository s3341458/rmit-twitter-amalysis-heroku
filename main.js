
function drawPie(data){
    "use strict";
    var width = 300,
        height = 300,
        radius = Math.min(width,height)/2;

    var color = d3.scale.ordinal()
        .range(["red", "green", "blue", "orange", "yellow", "navy", "gray"]);
    var arc = d3.svg.arc()
        .outerRadius(radius)
        .innerRadius(radius-80);
    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d){
            return d.count;
        });

    var svg = d3.select(".piechart").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
        .data(pie(data.cash))
        .enter().append("g")
        .attr("class","arc");

    g.append("path")
        .attr("d", arc)
        .attr("stroke","white")
        .style("fill", function(d){
            return color(d.data.count);
        });

    g.append("text")
        .attr("transform", function(d){
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("dy", ".35em")
        .style("text-anchor","middle")
        .text(function(d){
            return Math.round(d.data.count);
        });

    var details = d3.select(".details")
        .append("ul")
        .selectAll("li")
        .data(data.cash)
        .enter()
        .append("li")
        .text(function(d){
            return d.name;
        });


    var legend = d3.select(".legend")
        .append("svg")
        .selectAll("g")
        .data(pie(data.cash))
        .enter().append("g")
        .attr("transform", function(d, i){
                return "translate(0 " + i * 20 + ")";
        });

    legend.append("rect")
        .attr("width", 40)
        .attr("height", 15)
        .style("fill", function(d){
            return color(d.data.count);
        });
}

function initDraw(){
    d3.json('data/plaza_traffic.json',drawPie);
}

$(function(){

    $.getJSON("data/plaza_traffic.json", function(d){
        var posRatio = d.ratio[0].positiveRatio,
            negRatio = d.ratio[0].negRatio,
            posEle = $(".posRate"),
            negEle = $(".negRate"),
            initNum = 0;
        numberAutoIncreasing(initNum, posEle, posRatio);
        numberAutoIncreasing(initNum, negEle, negRatio);
        function numberAutoIncreasing(initNum, ele, ratio) {
            var interval = setInterval(function(){
                initNum++;

                ele.text(initNum++ + ".00%");
                if (initNum >= ratio) {
                    clearInterval(interval)
                    ele.text(ratio + "0%");
                }
            },50);
        }

    });
    $("#posBtn, #searchbox, #negBtn, #pieChart").tooltip();
    initDraw();
});

//$('.btn-danger').on('click',function(){
//        $('.legend, .details').slideToggle('slow');
//    });


//show ration
