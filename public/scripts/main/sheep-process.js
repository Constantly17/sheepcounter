document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const imageInput = document.getElementById("imageInput");
    const resultImage = document.getElementById("resultImage");
    const stats = document.getElementById("stats");

    uploadForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const file = imageInput.files[0];
        if (!file) {
            alert("Пожалуйста, выберите изображение.");
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        try {
            const response = await fetch("/process", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Ошибка загрузки: " + response.status);
            }

            const data = await response.json();

            if (data.status === "success") {
                resultImage.src = "/media/results/" + data.image_filename;
				resultImage.style.display = "block";
                stats.textContent = "Обнаружено овец: " + data.sheep_count;
            } else {
                alert("Ошибка: " + data.message);
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при обработке изображения.");
        }
    });
});
