const form = document.getElementById('traceForm');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultsDiv = document.getElementById('results');
const hopsTableBody = document.getElementById('hopsTableBody');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const destination = document.getElementById('destination').value;
    const max_hops = document.getElementById('max_hops').value;

    // Reset UI
    loading.style.display = 'block';
    errorDiv.style.display = 'none';
    resultsDiv.style.display = 'none';
    hopsTableBody.innerHTML = '';

    try {
        const response = await fetch('/trace', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({destination, max_hops})
        });

        const data = await response.json();
        loading.style.display = 'none';

        if (!data.success) {
            errorDiv.innerText = data.error;
            errorDiv.style.display = 'block';
            return;
        }

        // Fill header info
        document.getElementById('result-destination').innerText = data.destination;
        document.getElementById('result-ip').innerText = data.dest_ip;
        document.getElementById('result-hops').innerText = data.total_hops;
        document.getElementById('result-status').innerText = data.reached ? 'Reached' : 'Unreachable';

        // Fill table rows
        data.hops.forEach(hop => {
            let rttStr = hop.avg_rtt !== null ? hop.avg_rtt.toFixed(2) : '*';
            let ipStr = hop.ip || '*';
            let hostnameStr = hop.hostname || 'Timeout';
            let locationStr = hop.location 
                ? `${hop.location.city}, ${hop.location.country}` 
                : '*';

            const row = document.createElement('tr');

            if (hop.ip === data.dest_ip) row.classList.add('destination-row');

            row.innerHTML = `
                <td>${hop.ttl}</td>
                <td class="${hop.ip ? '' : 'timeout'}">${ipStr}</td>
                <td>${hostnameStr}</td>
                <td class="location">${locationStr}</td>
                <td class="rtt-values">${rttStr}</td>
            `;
            hopsTableBody.appendChild(row);
        });

        resultsDiv.style.display = 'block';

    } catch (err) {
        loading.style.display = 'none';
        errorDiv.innerText = err.message;
        errorDiv.style.display = 'block';
    }
});

function setDestination(dest) {
    document.getElementById('destination').value = dest;
}
