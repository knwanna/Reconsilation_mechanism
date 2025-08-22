const { app, BrowserWindow } = require('electron');
const path = require('path');
const log = require('electron-log');

log.transports.file.level = 'info';

const createWindow = () => {
  try {
    const win = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: false,
        contextIsolation: true,
        sandbox: true
      }
    });

    win.loadFile(path.join(__dirname, 'index.html'));

    win.on('closed', () => {
      log.info('Main window closed');
    });

    return win;
  } catch (error) {
    log.error(Failed to create window: );
    app.quit();
  }
};

app.whenReady().then(() => {
  const win = createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
}).catch(error => {
  log.error(App failed to start: );
  app.quit();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
