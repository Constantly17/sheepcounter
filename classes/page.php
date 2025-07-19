<?php
        session_start();	
require_once $_SERVER['ROOT_PATH'] . '/classes/db.php';
global $conn;
$conn = new Database();

class Page {
    private string $pageTitle = 'Автоматический подсчет овец';
    private string $pageHeader = 'Подсчет овец на пастбище';
    private array $styles = [];
    private array $scripts = [];
    private array $customContent = [];
    private bool $navbar = true;
    private bool $footer = true;

    public function renderPage(): void {
        echo '<!DOCTYPE html>';
        echo '<html lang="ru">';
        echo $this->renderHead();
        echo '<body class="d-flex flex-column min-vh-100">';
        echo $this->renderNavbar();
        echo '<main class="flex-grow-1 py-4"><div class="container">';
        echo '<h1 class="mb-4">' . htmlspecialchars($this->pageHeader) . '</h1>';
        echo $this->renderCustomContent();
        echo '</div></main>';
        echo $this->renderFooter();
        echo $this->renderScripts();
        echo '</body></html>';
    }

    public function setPageTitle(string $title): self {
        $this->pageTitle = htmlspecialchars($title);
        return $this;
    }

    public function addStyle(string $style): self {
        $this->styles[] = $style;
        return $this;
    }

    public function addScript(string $script): self {
        $this->scripts[] = $script;
        return $this;
    }

    public function addCustomContent(string $content): self {
        $this->customContent[] = $content;
        return $this;
    }

    private function renderHead(): string {
        $out = '<head>';
        $out .= '<meta charset="UTF-8">';
        $out .= '<meta name="viewport" content="width=device-width, initial-scale=1">';
        $out .= '<title>' . $this->pageTitle . '</title>';
        $out .= '<link rel="icon" type="image/svg+xml" href="/media/logo-enter.svg">';
        $out .= '<link href="/css/bootstrap.min.css" rel="stylesheet">';
        $out .= '<link href="/css/bootstrap-icons.css" rel="stylesheet">';
        foreach ($this->styles as $style) {
            $out .= '<link rel="stylesheet" href="/css/main/' . htmlspecialchars($style) . '">';
        }
        $out .= '</head>';
        return $out;
    }

    private function renderScripts(): string {
        $out = '<script src="/scripts/bootstrap.bundle.min.js"></script>';
        foreach ($this->scripts as $script) {
            $out .= '<script src="/scripts/main/' . htmlspecialchars($script) . '"></script>';
        }
        return $out;
    }

    private function renderNavbar(): string {
		if (!$this->navbar) return '';
		return '
		<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm">
			<div class="container">
				<a class="navbar-brand text-primary fw-bold" href="/">🐑 SheepCounter</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
						aria-controls="navbarNav" aria-expanded="false" aria-label="Переключить навигацию">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarNav">
					<ul class="navbar-nav me-auto">
						<li class="nav-item"><a class="nav-link text-dark" href="/">Главная</a></li>
						<li class="nav-item"><a class="nav-link text-dark" href="https://github.com/your-repo" target="_blank">GitHub</a></li>
					</ul>
				</div>
			</div>
		</nav>
		';
	}

    private function renderFooter(): string {
		if (!$this->footer) return '';
		return '
		<footer class="bg-light text-muted py-4 mt-auto border-top">
			<div class="container text-center small">
				&copy; ' . date('Y') . ' SheepCounter · Все права защищены
			</div>
		</footer>
		';
	}

    private function renderCustomContent(): string {
        return implode('', $this->customContent);
    }
}
