document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("uploadForm");
    const imageInput = document.getElementById("imageInput");
    const loading = document.getElementById("loadingIndicator");
    const stats = document.getElementById("stats");
    const resultImage = document.getElementById("resultImage");
    const countValue = document.getElementById("countValue");
    const timeValue = document.getElementById("timeValue");
    const imageLink = document.getElementById("imageLink");
    const reportBtn = document.getElementById("reportBtn");
    const pdfDownloadLink = document.getElementById("pdfDownloadLink");
    const resultJsonFilename = document.getElementById("resultJsonFilename");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const file = imageInput.files[0];
        if (!file) {
            alert("Пожалуйста, выберите изображение.");
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        loading.style.display = "block";
        stats.style.display = "none";
        reportBtn.style.display = "none";
        pdfDownloadLink.style.display = "none";

        const start = performance.now();

        try {
            const response = await fetch("/flask/process", {
                method: "POST",
                body: formData
            });

            const end = performance.now();
            const duration = Math.round(end - start);

            const data = await response.json();
            if (data.status !== "success") throw new Error(data.message || "Ошибка обработки");

            // Отображение результата
            resultImage.src = "/media/results/" + data.image_filename;
            resultImage.style.display = "block";
            countValue.textContent = data.sheep_count ?? "—";
            timeValue.textContent = duration;
            imageLink.href = "/media/results/" + data.image_filename;

            // Сохраняем имя JSON-файла
            resultJsonFilename.value = data.result_filename;

            // Показываем кнопки
            reportBtn.style.display = "inline-block";
            stats.style.display = "block";
        } catch (err) {
            alert("Ошибка: " + err.message);
        } finally {
            loading.style.display = "none";
        }
    });

    reportBtn.addEventListener("click", async () => {
        const filename = resultJsonFilename.value;
        if (!filename) {
            alert("Не удалось получить имя файла результата");
            return;
        }

        try {
            const response = await fetch("/flask/report", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ filename })
            });

            const data = await response.json();
			console.log('data', data);
            if (data.status !== "success") throw new Error(data.message || "Ошибка генерации отчета");

            pdfDownloadLink.href = "/media/results/" + data.report_filename;
            pdfDownloadLink.style.display = "inline-block";
        } catch (err) {
            alert("Ошибка при создании PDF: " + err.message);
        }
    });
});
