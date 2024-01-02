<script>
  import {onMount} from 'svelte';
  import {Chart, registerables} from 'chart.js';
  Chart.register(...registerables);

  let chart;
  let ibiChart;
  let analysisText = '';
  let data = [];

  async function fetchData() {
  try {
  const response = await fetch('http://172.20.10.4:5000/getdata');
  if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`);
}
  data = await response.json();
  console.log(data);

  const analysisResponse = await fetch('http://172.20.10.4:5000/getanalysis');
  if (!analysisResponse.ok) {
  throw new Error(`HTTP error! status: ${analysisResponse.status}`);
}
  const analysisData = await analysisResponse.json();
  analysisText = analysisData.length > 0 ? analysisData[analysisData.length - 1][1] : 'No analysis data available';
} catch (error) {
  console.error("Fetch error: ", error.message);
}
}

  function createChart(ctx, datasets) {
  return new Chart(ctx, {
  type: 'line',
  data: {
  labels: data.map(d => {
  const date = new Date(d[6] * 1000);
  return date.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'});
}),
  datasets: datasets
},
  options: {
  responsive: true,
  maintainAspectRatio: false
},
  scales: {
  y: {
  beginAtZero: true
}
}
}
  );
}

  onMount(async () => {
  await fetchData();

  const mainCtx = document.getElementById('mainChart').getContext('2d');
  chart = createChart(mainCtx, [
{
  label: 'Heart Rate',
  data: data.map(d => d[1]),
  borderColor: 'rgb(75, 192, 192)',
  tension: 0.1
},
{
  label: 'RMSSD',
  data: data.map(d => d[3]),
  borderColor: 'rgb(75, 75, 192)',
  tension: 0.1
},
{
  label: 'SDNN',
  data: data.map(d => d[4]),
  borderColor: 'rgb(192, 192, 75)',
  tension: 0.1
},
{
  label: 'Stress Score',
  data: data.map(d => d[5]),
  borderColor: 'rgb(75, 192, 75)',
  tension: 0.1
}
  ]);

  const ibiCtx = document.getElementById('ibiChart').getContext('2d');
  ibiChart = createChart(ibiCtx, [
{
  label: 'IBI',
  data: data.map(d => d[2]),
  borderColor: 'rgb(192, 75, 75)',
  tension: 0.1
}]);
  onDestroy(() => {
  if (chart) {
  chart.destroy();
}
  if (ibiChart) {
  ibiChart.destroy();
}
});
});
</script>

<div className="chart-container" style="position: relative; height:40vh; width:100vw padding: 20px">
  <canvas class="graph" id="mainChart"></canvas>
  <canvas class="graph" id="ibiChart"></canvas>
  <textarea readOnly style="width:100vw">
    {analysisText}
</textarea>
</div>

