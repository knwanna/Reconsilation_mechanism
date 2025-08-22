async function search() {
    const query = document.getElementById('query').value;
    const resultsDiv = document.getElementById('results');
    try {
        const response = await window.api.sendQuery(query);
        resultsDiv.innerHTML = '<h2>Results:</h2>' + JSON.stringify(response.result, null, 2);
    } catch (error) {
        resultsDiv.innerHTML = '<p>Error: ' + error.message + '</p>';
    }
}
