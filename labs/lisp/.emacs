(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(backup-directory-alist (quote (("." . "~/.emacs-backups"))))
 '(tab-width 4)
 '(c-basic-offset 4)
 '(column-number-mode t)
 '(default-input-method "latin-1-postfix")
 '(global-font-lock-mode t nil (font-lock))
 '(gud-gdb-command-name "gdb --annotate=1")
 '(inhibit-splash-screen t)
 '(large-file-warning-threshold nil)
 '(safe-local-variable-values (quote ((TeX-master . "Master"))))
 '(save-place t nil (saveplace))
 '(sentence-end-double-space nil)
 '(show-paren-mode t nil (paren))
 '(show-trailing-whitespace t))

(autoload 'longlines-mode "longlines.el"
 "Minor mode for automatically wrapping long lines." t)

(require 'ido)
(ido-mode t)
(setq ido-enable-flex-matching t) ;; enable fuzzy matching)

(add-to-list 'auto-mode-alist '("\\.js\\'" . espresso-mode))
(autoload 'espresso-mode "espresso" nil t)

(setq-default indent-tabs-mode nil)
(add-hook 'write-file-hooks
         (lambda ()
           (if (not indent-tabs-mode)
               (untabify (point-min) (point-max)))
           (delete-trailing-whitespace)))


;; From http://stackoverflow.com/questions/92971/how-do-i-set-the-size-of-emacs-window
(defun set-frame-size-according-to-resolution ()
  (interactive)
  (if window-system
  (progn
    ;; use 120 char wide window for largeish displays
    ;; and smaller 80 column windows for smaller displays
    ;; pick whatever numbers make sense for you
    (if (> (x-display-pixel-width) 1280)
        (add-to-list 'default-frame-alist (cons 'width 120))
      (add-to-list 'default-frame-alist (cons 'width 80)))
    ;; for the height, subtract a couple hundred pixels
    ;; from the screen height (for panels, menubars and
    ;; whatnot), then divide by the height of a char to
    ;; get the height we want
    (add-to-list 'default-frame-alist
                 (cons 'height (/ (- (x-display-pixel-height) 200) (frame-char-height)))))))

(set-frame-size-according-to-resolution)

(defun scroll-up-one ()
  (interactive)
  (scroll-up 1))

(defun scroll-down-one ()
  (interactive)
  (scroll-down 1))

(global-set-key "\C-z" 'scroll-up-one)
(global-set-key "\M-z" 'scroll-down-one)

(defun increase-indent ()
  (interactive)
  (if (< (point) (mark))
      (exchange-point-and-mark))
  (indent-rigidly (mark) (point) tab-width))

(defun decrease-indent ()
  (interactive)
  (if (< (point) (mark))
      (exchange-point-and-mark))
  (indent-rigidly (mark) (point) (- tab-width)))

(global-set-key "\M-[" 'decrease-indent)
(global-set-key "\M-]" 'increase-indent)
