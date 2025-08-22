async function performReconciliation() {
  const queryInput = document.getElementById('query-input').value.trim();
  const apiUrl = document.getElementById('api-url-input').value.trim() || 'http://localhost:8000';
  const statusDiv = document.getElementById('status-message');
  const resultsBody = document.getElementById('results-body');
  const resultsTable = document.getElementById('results-table');

  if (!queryInput) {
    statusDiv.textContent = 'Please enter a query string.';
    return;
  }

  statusDiv.textContent = 'Loading...';
  resultsBody.innerHTML = '';
  resultsTable.classList.add('hidden');

  try {
    const response = await fetch(${apiUrl}/reconcile?query=);

    if (!response.ok) {
      throw new Error(HTTP error! Status: );
    }

    const data = await response.json();
    const results = data.result || [];

    if (results.length === 0) {
      statusDiv.textContent = 'No matches found.';
      return;
    }

    results.forEach(result => {
      const row = document.createElement('tr');
      row.innerHTML = 
        <td class="border p-2"></td>
        <td class="border p-2"></td>
        <td class="border p-2"></td>
      ;
      resultsBody.appendChild(row);
    });

    resultsTable.classList.remove('hidden');
    statusDiv.textContent = 'Reconciliation complete.';
  } catch (error) {
    statusDiv.textContent = Error: ;
  }
}

document.getElementById('reconcile-btn').addEventListener('click', performReconciliation);
