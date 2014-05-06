
function drawPie(data){
    "use strict";
    var width = 260,
        height = 200,
        radius = Math.min(width,height)/2;

    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    var arc = d3.svg.arc()
        .outerRadius(radius-10)
        .innerRadius(0);
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

}

function showRatio(posRate,negRate){
    "use restrict";
    d3.select(".posRate")
        .text(posRate + "%");

    d3.select(".negRate")
        .text(negRate + "%");
}

function initDraw(){
    var posRate = 49.3,
        negRate = 50.7;
    showRatio(posRate,negRate);
    d3.json('data/plaza_traffic.json',drawPie);

}



$('.btn-danger').on('click',
    function(){
        $(this).parent().prev().slideToggle('slow');
    });