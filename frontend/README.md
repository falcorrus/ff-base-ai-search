# FF-BASE AI Search Frontend

Frontend application for the FF-BASE AI Search system.

## Technologies Used

- Vanilla JavaScript
- Tailwind CSS (via local build)
- Firebase Hosting

## Project Structure

```
.
├── index.html       # Main HTML file
├── script.js        # Main JavaScript file
├── server.js        # Express server for Firebase functions
├── package.json     # Project dependencies and scripts
└── ...
```

## Available Scripts

- `npm start` - Start the Node.js server
- `npm run start-python` - Start a Python HTTP server on port 3000
- `npm run deploy` - Deploy to Firebase Hosting
- `npm run build:css` - Build Tailwind CSS
- `npm run build` - Build all assets

## Development

To run the frontend locally:

1. Start the backend server (see backend README)
2. Run `npm start` to start the frontend server
3. Open `http://localhost:3000` in your browser

For easier development, you can use the `start-dev.sh` script in the root directory to start both backend and frontend simultaneously.

If you make changes to the styles, you can rebuild the CSS using:
```bash
./rebuild-css.sh
```

## shadcn/ui Integration

This project has been configured to use shadcn/ui components with a vanilla JavaScript setup. 
See `SHADCN_UI.md` for more information on how to use and extend the components.

## Deployment

To deploy to Firebase Hosting:

1. Run `npm run deploy`
2. The site will be available at the configured Firebase URL