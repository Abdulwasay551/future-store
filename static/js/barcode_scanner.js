// Function to handle barcode scanning
function initBarcodeScanner(inputFieldId) {
    let videoElement = null;
    let stream = null;

    async function startScanning() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
            
            // Create video element if it doesn't exist
            if (!videoElement) {
                const modal = document.createElement('div');
                modal.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 1000;';
                
                videoElement = document.createElement('video');
                videoElement.style = 'max-width: 100%; max-height: 100%;';
                
                const closeButton = document.createElement('button');
                closeButton.innerText = '×';
                closeButton.style = 'position: absolute; top: 20px; right: 20px; background: white; border: none; font-size: 24px; cursor: pointer; padding: 5px 10px; border-radius: 5px;';
                closeButton.onclick = stopScanning;
                
                modal.appendChild(videoElement);
                modal.appendChild(closeButton);
                document.body.appendChild(modal);
            }

            videoElement.srcObject = stream;
            videoElement.play();

            // Initialize barcode detection
            const barcodeDetector = new BarcodeDetector();
            
            // Continuous scanning
            async function scan() {
                if (!stream) return;
                
                try {
                    const barcodes = await barcodeDetector.detect(videoElement);
                    if (barcodes.length > 0) {
                        const barcode = barcodes[0];
                        document.getElementById(inputFieldId).value = barcode.rawValue;
                        stopScanning();
                        return;
                    }
                } catch (err) {
                    console.error("Barcode scanning error:", err);
                }
                
                requestAnimationFrame(scan);
            }
            
            scan();
            
        } catch (err) {
            console.error("Error accessing camera:", err);
            alert("Could not access the camera. Please check permissions.");
        }
    }

    function stopScanning() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        if (videoElement && videoElement.parentElement) {
            videoElement.parentElement.remove();
            videoElement = null;
        }
    }

    return {
        start: startScanning,
        stop: stopScanning
    };
}

// Function to add scanner button next to an input field
function addScannerButton(inputFieldId) {
    const inputField = document.getElementById(inputFieldId);
    if (!inputField) return;

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'scanner-button';
    button.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="7" y="7" width="10" height="10" rx="2"/></svg>';
    button.style = 'margin-left: 8px; padding: 4px; background: #007bff; border: none; border-radius: 4px; cursor: pointer; vertical-align: middle;';
    
    const scanner = initBarcodeScanner(inputFieldId);
    button.onclick = () => scanner.start();
    
    inputField.parentNode.insertBefore(button, inputField.nextSibling);
}

// Initialize scanner buttons when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // For DeviceIdentifier admin
    const identifierFields = document.querySelectorAll('[name$="-identifier_value"]');
    identifierFields.forEach(field => {
        if (field.id) {
            addScannerButton(field.id);
        }
    });
});
