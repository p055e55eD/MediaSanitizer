// frontend/js/main.js

document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Elements ---
    const urlSwitch = document.getElementById("urlSwitch");
    const textSwitch = document.getElementById("textSwitch");
    const urlInputGroup = document.getElementById("urlInputGroup");
    const textInputGroup = document.getElementById("textInputGroup");
    const form = document.getElementById("checkForm");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const API_ENDPOINT = "http://localhost:5000/api/analyze"; // Update if deploying!

    let inputMode = "url";

    // --- Input Mode Switch ---
    urlSwitch.addEventListener("click", () => setInputMode("url"));
    textSwitch.addEventListener("click", () => setInputMode("text"));

    function setInputMode(mode) {
        inputMode = mode;
        if (mode === "url") {
            urlSwitch.classList.add("active");
            textSwitch.classList.remove("active");
            urlInputGroup.style.display = "block";
            textInputGroup.style.display = "none";
            form.articleUrl.required = true;
            form.articleText.required = false;
        } else {
            urlSwitch.classList.remove("active");
            textSwitch.classList.add("active");
            urlInputGroup.style.display = "none";
            textInputGroup.style.display = "block";
            form.articleUrl.required = false;
            form.articleText.required = true;
        }
        clearErrors();
    }

    // --- Form Submit Handler ---
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        clearErrors();

        let value = "";
        if (inputMode === "url") {
            value = form.articleUrl.value.trim();
            if (!isValidUrl(value)) {
                showError("Please enter a valid news URL.");
                return;
            }
        } else {
            value = form.articleText.value.trim();
            if (value.length < 50) {
                showError("Please paste at least 50 characters of article text.");
                return;
            }
        }

        setLoading(true);

        const payload = {
            type: inputMode,
            content: value
        };

        try {
            const response = await fetch(API_ENDPOINT, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                let errorMsg = "An error occurred. Please try again.";
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch {}
                throw new Error(errorMsg);
            }

            const result = await response.json();

            // Double-check the result is not empty
            if (!result || typeof result !== "object") {
                throw new Error("No analysis result returned. Please try again.");
            }
            // Save analysis to sessionStorage
            sessionStorage.setItem("analysisResult", JSON.stringify(result));
            window.location.href = "results.html";

        } catch (error) {
            showError(error.message || "Failed to analyze. Please try again.");
            setLoading(false);
        }
    });

    // --- Helper Functions ---
    function isValidUrl(url) {
        try {
            const parsed = new URL(url);
            return ["http:", "https:"].includes(parsed.protocol);
        } catch {
            return false;
        }
    }

    function setLoading(loading) {
        if (loading) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = `<span class="spinner"></span> Analyzing...`;
        } else {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = `<span class="btn-text">Analyze Credibility</span>`;
        }
    }

    function showError(message) {
        clearErrors();
        const errorDiv = document.createElement("div");
        errorDiv.className = "error-message";
        errorDiv.textContent = message;
        form.parentNode.insertBefore(errorDiv, form);
    }

    function clearErrors() {
        document.querySelectorAll(".error-message").forEach(el => el.remove());
    }

    // --- Initialize ---
    setInputMode("url");
    setLoading(false);
});
