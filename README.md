# Математична пасіка (The Maths Apiary)

Ігри-уроки і живі шпаргалки для 6–7 класу, українською та англійською. Статичний сайт: лише HTML-файли й PDF, без сервера й бази даних.

## Що всередині

| Тема | Гра | Шпаргалка |
|---|---|---|
| Відсотки | `percentages/uk.html`, `percentages/en.html` | — |
| Пропорції | `proportions/uk.html`, `proportions/en.html` | `proportions/cheatsheet-*.html` і `.pdf` |
| Одночлени | `monomials/uk.html`, `monomials/en.html` | `monomials/cheatsheet-*.html` і `.pdf` |
| Степені | `powers/uk.html`, `powers/en.html` | `powers/cheatsheet-*.html` і `.pdf` |
| Суміжні кути | `angles/uk.html`, `angles/en.html` | `angles/cheatsheet-*.html` і `.pdf` |
| Тотожності й вирази | `identities/uk.html`, `identities/en.html` | `identities/cheatsheet-*.html` і `.pdf` |

Головна сторінка — `index.html` (українською) і `index-en.html` (англійською).

## Як опублікувати на GitHub Pages

1. На github.com натисніть **New repository**. Назва, наприклад, `matematyka`. Тип — **Public** (на безкоштовному плані Pages працює з публічними репозиторіями).
2. У новому репозиторії: **Add file → Upload files**. Перетягніть усі файли й папки з цієї папки (не саму папку, а її вміст). Натисніть **Commit changes**.
3. **Settings → Pages**. У розділі *Build and deployment* виберіть *Source: Deploy from a branch*, гілку **main** і папку **/ (root)**. Натисніть **Save**.
4. За хвилину-дві сайт буде за адресою `https://<ваш-логін>.github.io/matematyka/`. Посилання з'явиться вгорі сторінки Settings → Pages.

Файл `.nojekyll` прихований; якщо він не завантажився, нічого страшного, сайт працюватиме й без нього.

## Як оновлювати

Щоб замінити сторінку, відкрийте її в репозиторії, натисніть **Add file → Upload files** і завантажте новий файл з тією самою назвою. Сайт оновиться сам за хвилину-дві.

## Прогрес і звіти

- Зірки й прогрес зберігаються в браузері учня (localStorage) на конкретному пристрої. Сайт нічого не збирає й нікуди не надсилає.
- Кнопка «Скопіювати звіт» у вкладці «Мій звіт» копіює текстовий звіт, який учень може вставити в повідомлення вчителеві чи батькам.
