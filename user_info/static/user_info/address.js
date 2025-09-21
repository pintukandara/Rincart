document.addEventListener("DOMContentLoaded", function () {
    const locationBtn = document.getElementById("getLocationBtn");

    if (locationBtn) {
        locationBtn.addEventListener("click", function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
            } else {
                alert("Geolocation is not supported by your browser.");
            }
        });
    }

    function successCallback(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Fetch location details from OpenStreetMap Nominatim API
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
            .then(response => response.json())
            .then(data => {
                console.log("Location data:", data);
                
                if (data.address) {
                    document.getElementById("id_city").value = data.address.city || data.address.town || "";
                    document.getElementById("id_pincode").value = data.address.postcode || "";
                    
                    document.getElementById("id_state").value = data.address.state || "";
                    
                }
            })
            .catch(error => {
                console.error("Error fetching location:", error);
                alert("Error getting location data. Please try again.");
            });
    }

    function errorCallback(error) {
        alert("Unable to retrieve your location: " + error.message);
    }
});
