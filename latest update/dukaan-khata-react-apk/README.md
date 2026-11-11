# Dukaan Khata — React + Android APK project

This project wraps your supplied `dukaan-khata.html` prototype in a React/Vite application and packages it for Android using Capacitor. The original mobile layout and its demo interactions are kept in `public/prototype.html`.

## 1. Requirements
- Node.js 18 or newer
- Android Studio (with Android SDK installed)
- Java/JDK version supported by your installed Android Studio/Gradle

## 2. Install and run in browser
Open this folder in VS Code / terminal and run:

```bash
npm install
npm run dev
```

Open the local URL shown by Vite. This is a demo prototype; login OTP, payment/UPI, reminders, backup and other integrations are simulated and are not connected to a live server.

## 3. Create the Android project
Run these commands from this folder:

```bash
npm install
npm run build
npx cap add android
npx cap sync android
npx cap open android
```

In Android Studio:
1. Wait for Gradle sync to finish.
2. Select **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
3. When the build completes, click **locate** in the notification to find the APK.
4. For a release APK, use **Build > Generate Signed Bundle / APK** and follow the signing wizard.

The debug APK is normally created at:
`android/app/build/outputs/apk/debug/app-debug.apk`

## 4. After changing the UI
Update `public/prototype.html`, then run:

```bash
npm run build
npx cap sync android
```

Reopen Android Studio and build the APK again.

## Notes
- This is a React shell with the supplied HTML prototype embedded in a full-screen iframe, preserving the current prototype behavior while making it buildable as an Android app.
- Data in the prototype is demo data stored in browser local storage. For production use, connect a secure backend/database and replace demo OTP/payment behavior with real providers.
- An APK is not prebuilt here because Android SDK/Gradle signing and build tools are required; this ZIP contains the source project and setup steps to generate it locally.


## 5. Payments & Statements prototype
The More menu includes **Payments & Statements** with Google Pay, PhonePe, other UPI and bank-statement source labels. The screen supports manual transaction entry, importing CSV transaction files, filtering the history, and downloading the combined history as CSV. Sample rows are clearly demo data and are stored locally in the app's browser storage.

Important: this is a UI/prototype integration, not a live connection to GPay, PhonePe, or a bank. Use CSV exports where available. The current demo does not parse PDF statements or connect to bank APIs. Never collect a UPI PIN, banking password, or OTP in this app. For production integration, use a compliant provider/bank-approved flow and secure backend.
