
var firstBlockName = JSON.parse(document.getElementById('first_block').textContent);
var firstBlockOnline = JSON.parse(document.getElementById('first_block_online').textContent);

var secondBlockName = JSON.parse(document.getElementById('second_block').textContent);
var secondBlockOnline = JSON.parse(document.getElementById('second_block_online').textContent);

const ctx = document.getElementById('blockChart');

new Chart(ctx, {
    type: 'bar',
    data: {
    labels: [firstBlockName, secondBlockName],
    datasets: [{
        label: '# online users',
        data: [firstBlockOnline, secondBlockOnline],
        borderWidth: 1
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});

