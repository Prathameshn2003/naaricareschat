# NaariCare - Women's Health Assistant

AI-powered women's health and wellness app with PCOS, menstrual cycle, and menopause tracking. Built as a Progressive Web App (PWA) for mobile-first experience.

## 🚀 Features

- **PCOS Risk Assessment**: AI-powered prediction with personalized recommendations
- **Menstrual Cycle Tracking**: Smart cycle prediction and irregularity detection
- **Menopause Support**: Symptom tracking and stage identification
- **Mobile-First PWA**: Installable app experience on any device
- **Offline Support**: Core functionality works without internet
- **Responsive Design**: Optimized for all screen sizes

## 🛠️ Tech Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Shadcn/ui
- **Backend**: FastAPI + Python + ML models (scikit-learn, TensorFlow, XGBoost)
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Vercel (Frontend) + Render (Backend)
- **PWA**: Vite PWA plugin for mobile app experience

## 📱 Progressive Web App (PWA)

This app can be installed on mobile devices and works offline:

1. **Install on Mobile**: Open in browser → Add to Home Screen
2. **Offline Access**: Core features work without internet
3. **Native Feel**: App-like experience with push notifications
4. **Cross-Platform**: Works on iOS, Android, and desktop

## 🚀 Deployment

### Backend (Render)

1. **Create Render Account**: https://render.com
2. **Connect Repository**: Link your GitHub repo
3. **Deploy Backend**:
   - Service Type: Web Service
   - Runtime: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable: `TF_CPP_MIN_LOG_LEVEL=3`
4. **Get Backend URL**: Copy the service URL (e.g., `https://naari-care-backend.onrender.com`)

### Frontend (Vercel)

1. **Create Vercel Account**: https://vercel.com
2. **Connect Repository**: Import your GitHub repo
3. **Configure Environment Variables**:
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   VITE_ML_API_URL=https://your-render-backend-url.onrender.com
   ```
4. **Deploy**: Vercel will auto-deploy on git push

### PWA Setup

The app is already configured as a PWA. To customize icons:

1. Replace placeholder icons in `/public/`:
   - `pwa-192x192.png` (192x192)
   - `pwa-512x512.png` (512x512)
2. Update manifest in `vite.config.ts`
3. Rebuild and redeploy

## 🏃‍♀️ Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Setup

```bash
# Clone repository
git clone <your-repo-url>
cd naari-care-app

# Install frontend dependencies
npm install

# Setup backend
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Start backend (from backend directory)
uvicorn main:app --host 127.0.0.1 --port 8001

# Start frontend (from root directory)
npm run dev
```

### Environment Variables

Create `.env` file in root directory:

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_ML_API_URL=http://127.0.0.1:8001  # For local development
```

## 📊 API Endpoints

- `GET /` - Health check
- `POST /ml-predict` - ML predictions
  - Body: `{ "model_type": "pcos|menopause|cycle", "input_data": {...} }`

## 🔧 Build & Test

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Test backend API
cd backend
python test_api.py
```

## 📱 Mobile Installation

Users can install the app on their devices:

1. **Open the deployed app** in a mobile browser
2. **Add to Home Screen**:
   - iOS: Share → Add to Home Screen
   - Android: Menu → Add to Home Screen
3. **Launch from home screen** like a native app

## 🎯 Performance Optimization

- **Lazy Loading**: Components load on demand
- **Code Splitting**: Automatic chunk splitting
- **Caching**: Service worker caches resources
- **Compression**: Gzip compression enabled
- **CDN**: Assets served via Vercel's CDN

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For support, email support@naari.care or join our community forum.

---

Made with ❤️ for women's health and wellness
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

