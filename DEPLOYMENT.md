# راهنمای نصب Foti Bot روی VPS

## نصب سریع (یک دستور)

```bash
cd /opt && git clone https://github.com/moha100h/foti.git foti && cd foti && sudo bash install.sh
```

> بات در `/opt/foti` نصب می‌شود — با سایر بات‌ها **هیچ تداخلی** ندارد.

---

## مدیریت بات

```bash
systemctl status foti       # وضعیت
systemctl start foti        # شروع
systemctl stop foti         # توقف
systemctl restart foti      # ری‌استارت
journalctl -u foti -f       # لاگ زنده
journalctl -u foti -n 100   # ۱۰۰ خط آخر لاگ
```

---

## آپدیت

```bash
cd /opt/foti
git pull origin main
source venv/bin/activate
pip install -r requirements.txt -q
python -m alembic upgrade head
systemctl restart foti
```

---

## ساختار پروژه

```
/opt/foti/
├── football_bot/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── handlers/
│   ├── keyboards/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── middleware/
├── migrations/
├── logs/
├── .env
├── install.sh
└── requirements.txt
```

---

## منابع داده رایگان

| منبع | پوشش | محدودیت |
|------|------|---------|
| football-data.org | لیگ‌های اروپایی | ۱۰ req/min |
| api-football (RapidAPI) | همه لیگ‌ها | ۱۰۰ req/day |
| OpenLigaDB | بوندسلیگا | بدون محدودیت |
| TheSportsDB | آمار تیم‌ها | رایگان |
| ESPN API | اخبار + نتایج | رایگان |

---

## عیب‌یابی

```bash
journalctl -u foti -p err -n 50
sudo -u postgres psql -c "\l"
redis-cli ping
ss -tlnp | grep -E '5432|6379|8000'
```
