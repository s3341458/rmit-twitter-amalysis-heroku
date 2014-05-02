
function drawPie(data){
    "use strict";
    var width = 300,
        height = 300,
        radius = Math.min(width,height)/2;

    var color1 = d3.scale.ordinal()
        .range(["red", "green", "blue", "orange", "yellow", "navy", "gray"]);

    var color2 = d3.scale.ordinal()
        .range(["red", "green", "blue", "orange", "yellow", "navy", "gray"]);
    var arc = d3.svg.arc()
        .outerRadius(radius)
        .innerRadius(radius-80);
    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d){
            return d.count;
        });
    //pos chart
    var svg = d3.select(".pospiechart").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
        .data(pie(data.positiveCountRegion))
        .enter().append("g")
        .attr("class","arc");

    g.append("path")
        .attr("d", arc)
        .attr("stroke","white")
        .style("fill", function(d){
            return color1(d.data.count);
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

    //neg chart
    var svg = d3.select(".negpiechart").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
        .data(pie(data.negativeCountRegion))
        .enter().append("g")
        .attr("class","arc");

    g.append("path")
        .attr("d", arc)
        .attr("stroke","white")
        .style("fill", function(d){
            return color2(d.data.count);
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
    //pos details
    var details1 = d3.select(".posdetails")
        .append("ul")
        .selectAll("li")
        .data(data.positiveCountRegion)
        .enter()
        .append("li")
        .text(function(d){
            return d.name;
        });
    //neg details
    var details2 = d3.select(".negdetails")
        .append("ul")
        .selectAll("li")
        .data(data.negativeCountRegion)
        .enter()
        .append("li")
        .text(function(d){
            return d.name;
        });
    //pos tweets
    var postweets = d3.select(".postweets")
        .append("h3")
        .selectAll("h3")
        .data(data.topPositiveTweets)
        .enter()
        .append("h3")
        .text(function(d){
            return  d;
        });
    //pos tweets
    var negtweets = d3.select(".negtweets")
        .append("h3")
        .selectAll("h3")
        .data(data.topNegativeTweets)
        .enter()
        .append("h3")
        .text(function(d){
            return d;
        });


    //pos legend
    var legend1 = d3.select(".poslegend")
        .append("svg")
        .selectAll("g")
        .data(pie(data.positiveCountRegion))
        .enter().append("g")
        .attr("transform", function(d, i){
                return "translate(0 " + i * 20 + ")";
        });

    legend1.append("rect")
        .attr("width", 40)
        .attr("height", 15)
        .style("fill", function(d){
            return color1(d.data.count);
        });

    //neg legend

    var legend2 = d3.select(".neglegend")
        .append("svg")
        .selectAll("g")
        .data(pie(data.negativeCountRegion))
        .enter().append("g")
        .attr("transform", function(d, i){
            return "translate(0 " + i * 20 + ")";
        });


    legend2.append("rect")
        .attr("width", 40)
        .attr("height", 15)
        .style("fill", function(d){
            return color2(d.data.count);
        });
}

function initDraw(){
    d3.json('/static/data/test.json',drawPie);
}

$(function(){

    $.getJSON("/static/data/test.json", function(d){
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
                    ele.text(ratio + "%");
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
