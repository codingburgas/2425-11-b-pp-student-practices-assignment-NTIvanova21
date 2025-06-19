bb.generate({
    data: {
        columns: [
            ["Approved", donutData.approved],
            ["Not Approved", donutData.notApproved]
        ],
        type: "donut",
        colors: {
            "Approved": "#006A71",
            "Not Approved": "#B4D4FF"
        },
        onclick: function(d) {
            console.log("clicked", d);
        },
        onover: function(d) {
            console.log("mouseover", d);
        },
        onout: function(d) {
            console.log("mouseout", d);
        }
    },
    donut: {
        title: `Total: ${donutData.total}`,
        label: {
            format: function(value, ratio, id) {
                return `${(ratio * 100).toFixed(1)}%\n(${value})`;
            },
            show: true
        },
        expand: true
    },
    tooltip: {
        format: {
            value: function(value, ratio, id) {
                return `${value} (${(ratio * 100).toFixed(1)}%)`;
            }
        }
    },
    size: {
        width: 500,
        height: 400
    },
    padding: {
        top: 20,
        right: 20,
        bottom: 20,
        left: 20
    },
    transition: {
        duration: 500
    },
    bindto: "#donut-chart"
});

// Bar Chart Configuration
const categories = [];
const approvedData = ["Approved"];
const notApprovedData = ["Not Approved"];

educationData.forEach(row => {
    categories.push(row[0]);
    approvedData.push(row[1]);
    notApprovedData.push(row[2]);
});

bb.generate({
    data: {
        columns: [
            approvedData,
            notApprovedData
        ],
        type: "bar",
        groups: [
            ["Approved", "Not Approved"]
        ],
        colors: {
            "Approved": "#006A71",
            "Not Approved": "#B4D4FF"
        },
        onclick: function(d) {
            console.log("clicked", d);
        }
    },
    bar: {
        width: {
            ratio: 0.7
        },
        padding: 3,
        radius: {
            ratio: 0.2
        }
    },
    axis: {
        x: {
            type: "category",
            categories: categories,
            tick: {
                rotate: -45,
                multiline: false,
                tooltip: true
            }
        },
        y: {
            label: {
                text: "Number of Applications",
                position: "outer-middle"
            },
            tick: {
                format: function(x) { return Math.floor(x); }
            }
        }
    },
    grid: {
        y: {
            show: true,
            lines: [
                {value: 0}
            ]
        }
    },
    legend: {
        padding: 10,
        item: {
            tile: {
                width: 15,
                height: 15
            }
        }
    },
    tooltip: {
        grouped: true,
        format: {
            title: function(x) {
                return `Education: ${categories[x]}`;
            },
            value: function(value, ratio, id) {
                return `${value} applications`;
            }
        }
    },
    size: {
        width: 500,
        height: 400
    },
    padding: {
        top: 40,
        right: 40,
        bottom: 60,
        left: 50
    },
    transition: {
        duration: 500
    },
    bindto: "#bar-chart"
});
