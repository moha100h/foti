# راهنمای کامل نصب و مدیریت Foti Bot روی VPS

## پیش‌نیازها
- Ubuntu 22.04 LTS (تست‌شده)
- دسترسی root
- حداقل 1GB RAM / 10GB Disk
- توکن بات از @BotFather
- آیدی عددی ادمین (از @userinfobot بگیرید)

---

## نصب سریع — یک دستور

```bash
cd /opt && git clone https://github.com/moha100h/foti.git foti && cd foti && sudo bash install.sh
```

> بات در `/opt/foti` نصب می‌شود.
> سرویس systemd با نام **`foti`** اجرا می‌شود — با سایر بات‌ها **هیچ تداخلی** ندارد.

---

## مراحل نصب دستی (اگر install.sh اجرا نشد)

```bash
# 1. نصب پیش‌نیازها
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev     postgresql postgresql-contrib redis-server git build-essential libpq-dev tzdata

# 2. کلون پروژه
sudo mkdir -p /opt/foti
cd /opt/foti
git clone https://github.com/moha100h/foti.git .

# 3. محیط مجازی Python
python3.11 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 4. دیتابیس
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE USER foti WITH PASSWORD 'YOUR_PASS';"
sudo -u postgres psql -c "CREATE DATABASE foti_db OWNER foti;"

# 5. فایل .env
cp .env.example .env
nano .env   # مقادیر را پر کنید

# 6. مهاجرت دیتابیس
./venv/bin/python -m alembic upgrade head

# 7. اجرای بات
./venv/bin/python -m football_bot.main
```

---

## مدیریت سرویس

```bash
systemctl status foti        # وضعیت
systemctl start foti         # شروع
systemctl stop foti          # توقف
systemctl restart foti       # ری‌استارت
journalctl -u foti -f        # لاگ زنده
journalctl -u foti -n 200    # ۲۰۰ خط آخر لاگ
journalctl -u foti -p err    # فقط خطاها
```

---

## آپدیت بات

```bash
cd /opt/foti
git pull origin main
./venv/bin/pip install -r requirements.txt -q
./venv/bin/python -m alembic upgrade head
systemctl restart foti
```

---

## ساختار پروژه

```
/opt/foti/
├── football_bot/
│   ├── __init__.py
│   ├── main.py              # نقطه ورود — asyncio.run(main())
│   ├── config.py            # تنظیمات از .env با pydantic-settings
│   ├── database.py          # SQLAlchemy async engine + Base
│   ├── handlers/
│   │   ├── __init__.py      # تجمیع همه روترها
│   │   ├── start.py         # /start و /help
│   │   ├── live.py          # نتایج زنده
│   │   ├── fixtures.py      # برنامه بازی‌ها
│   │   ├── predictions.py   # پیش‌بینی‌ها
│   │   ├── worldcup.py      # جام جهانی 2026
│   │   ├── stats.py         # آمار
│   │   └── admin.py         # پنل ادمین (/admin)
│   ├── keyboards/
│   │   ├── main_menu.py     # منوی اصلی Reply
│   │   ├── live_menu.py     # دکمه refresh
│   │   ├── fixtures_menu.py # امروز/فردا/هفته
│   │   ├── predictions_menu.py
│   │   ├── worldcup_menu.py
│   │   ├── stats_menu.py
│   │   └── admin_menu.py
│   ├── models/
│   │   ├── user.py          # جدول users (PK: telegram_id)
│   │   ├── match.py         # جدول matches
│   │   ├── prediction.py    # جدول predictions
│   │   └── team.py          # جدول teams
│   ├── services/
│   │   ├── user_service.py      # get_or_create_user
│   │   ├── live_service.py      # TheSportsDB API
│   │   ├── fixtures_service.py  # TheSportsDB eventsday
│   │   ├── prediction_service.py
│   │   ├── worldcup_service.py
│   │   ├── stats_service.py
│   │   └── scheduler.py         # APScheduler (Asia/Tehran)
│   ├── middleware/
│   │   ├── db_middleware.py     # inject db session
│   │   └── rate_limit.py        # rate limiting per user
│   └── utils/
│       ├── formatting.py        # format_live_match, format_fixture, ...
│       └── helpers.py           # confidence_emoji, format_percent
├── migrations/
│   ├── env.py               # Alembic env (psycopg2 sync)
│   ├── script.py.mako
│   └── versions/
│       └── 0001_initial.py  # اولین migration — همه جداول
├── logs/                    # فایل‌های لاگ (loguru)
├── .env                     # تنظیمات محیطی (ساخته می‌شود)
├── .env.example             # نمونه تنظیمات
├── alembic.ini              # تنظیمات Alembic (psycopg2)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── install.sh
```

---

## متغیرهای محیطی (.env)

| متغیر | توضیح | مثال |
|-------|-------|------|
| `BOT_TOKEN` | توکن بات از @BotFather | `123456:ABC...` |
| `ADMIN_IDS` | آیدی عددی ادمین | `277236314` |
| `DATABASE_URL` | آدرس PostgreSQL (asyncpg) | `postgresql+asyncpg://foti:pass@localhost/foti_db` |
| `ALEMBIC_DATABASE_URL` | آدرس PostgreSQL (psycopg2 — فقط migration) | `postgresql+psycopg2://foti:pass@localhost/foti_db` |
| `REDIS_URL` | آدرس Redis | `redis://localhost:6379/0` |
| `ADMIN_API_KEY` | کلید API پنل ادمین | رندوم |
| `LOG_LEVEL` | سطح لاگ | `INFO` یا `DEBUG` |
| `RATE_LIMIT` | حداکثر پیام در پنجره زمانی | `60` |
| `RATE_LIMIT_WINDOW` | پنجره زمانی (ثانیه) | `60` |

---

## منابع داده رایگان

| منبع | پوشش | محدودیت رایگان | آدرس |
|------|------|----------------|------|
| TheSportsDB | نتایج زنده، برنامه | رایگان (v1) | thesportsdb.com |
| football-data.org | لیگ‌های اروپایی | ۱۰ req/min | football-data.org |
| OpenLigaDB | بوندسلیگا | بدون محدودیت | openligadb.de |
| ESPN API | اخبار + نتایج | رایگان | site.api.espn.com |

---

## عیب‌یابی

```bash
# خطاهای بات
journalctl -u foti -p err -n 50

# بررسی دیتابیس
sudo -u postgres psql -c "\l"
sudo -u postgres psql -d foti_db -c "\dt"

# بررسی Redis
redis-cli ping

# بررسی پورت‌ها
ss -tlnp | grep -E '5432|6379|8000'

# تست اتصال دیتابیس
cd /opt/foti && ./venv/bin/python -c "
import asyncio
from football_bot.database import init_db
asyncio.run(init_db())
print('DB OK')
"

# اجرای migration دستی
cd /opt/foti && ./venv/bin/python -m alembic upgrade head

# بررسی نسخه Python
/opt/foti/venv/bin/python --version
```

---

## نکات مهم

- **تداخل با سایر بات‌ها:** هر بات در `/opt/<name>` جداگانه نصب می‌شود و سرویس systemd جداگانه دارد — هیچ تداخلی نیست.
- **Alembic vs asyncpg:** بات از `asyncpg` استفاده می‌کند اما Alembic برای migration از `psycopg2` استفاده می‌کند — این طراحی عمدی است.
- **لاگ‌ها:** در `logs/foti.log` ذخیره می‌شوند و هر ۱۰MB چرخش می‌کنند.
- **Rate Limiting:** هر کاربر حداکثر ۶۰ پیام در ۶۰ ثانیه می‌تواند ارسال کند.
