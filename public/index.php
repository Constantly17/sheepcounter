<?php

require_once $_SERVER['ROOT_PATH'].'/classes/Page.php';

$page = new Page();
$page->addScript('main.js');
//$page->addScript('sheep-process.js');
$content = '';
$content .= '<div class="mb-3">
 
<form id="uploadForm">
 <label for="imageInput" class="form-label">Загрузите фото с овцами</label>
    <input type="file" id="imageInput" accept="image/jpeg,image/png,image/webp" class="form-control mb-3">
    <button type="submit" id="submitBtn" class="btn btn-primary">Обработать</button>
</form>
<div id="loadingIndicator" class="mt-3 text-warning fw-bold" style="display: none;">
    <div class="spinner-border text-primary me-2" role="status"></div>
    Обработка изображения…
</div>
<div id="stats" class="mt-4" style="display: none;">
    <img id="resultImage" src="" alt="Результат" class="img-fluid mb-3 border rounded shadow-sm">
    <ul class="list-group">
        <li class="list-group-item">Обнаружено овец: <span id="countValue"></span></li>
        <li class="list-group-item">Время ответа: <span id="timeValue"></span> мс</li>
        <li class="list-group-item">Файл: <a id="imageLink" href="#" download>Скачать</a></li>
    </ul>
</div>
<input type="hidden" id="resultJsonFilename">
<button id="reportBtn" class="btn btn-outline-success mt-3" style="display: none;">
    Сформировать PDF-отчёт
</button>
<a id="pdfDownloadLink" href="#" class="btn btn-success mt-2" style="display: none;" download>Скачать отчёт</a>
';
$page->addCustomContent($content);
$page->renderPage();

?>