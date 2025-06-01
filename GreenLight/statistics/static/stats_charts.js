bb.generate({
    data: {
        columns: [
            ["Approved", donutData.approved],
            ["Not Approved", donutData.notApproved]
        ],
        type: "donut"
    },
    donut: {
        title: `Total loan requests: ${donutData.total}`
    },
    size: {
        width: 500,
        height: 400
    },
    bindto: "#donut-chart"
});

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
        ]
    },
    bar: {
        width: {
            ratio: 0.5
        }
    },
    axis: {
        x: {
            type: "category",
            categories: categories
        }
    },
    size: {
        width: 500,
        height: 400
    },
    bindto: "#bar-chart"
});
