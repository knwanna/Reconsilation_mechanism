const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
    sendQuery: async (query) => {
        const response = await fetch('http://localhost:8000/reconcile?query=' + encodeURIComponent(query));
        return response.json();
    }
});
