# manobalsas-scraper

[manobalsas.lt](https://www.manobalsas.lt) has an awesome idea, however it lacks some analytical capabilities. This little project allows scraping whole site and using sqlite to gain more sophisticated insights.

## Prerequisites
[Install docker](https://docs.docker.com/get-started/get-docker/)

## Run db on pre-scraped data
```bash
docker-compose run db
```

## Run scraper yourself
It will replace existing db with newly scraped one. It can take a while...
```bash
docker-compose run scrape
```

## Example queries
Question averages by party:
```sql
SELECT
  P.party,
  Q.q_id,
  Q.question,
  AVG(A.answer)
FROM answers AS A
JOIN questions AS Q ON Q.q_id = A.q_id
JOIN politicians AS P ON P.id = A.pol_id
GROUP BY 1, 2, 3;
```
---
Answers for specific question:
```sql
SELECT
  P.party,
  P.name,
  A.answer
FROM answers AS A
JOIN questions AS Q ON Q.q_id = A.q_id
JOIN politicians AS P ON P.id = A.pol_id
WHERE A.q_id = 2
ORDER BY 3 DESC;
```

---

Question area matrix by party:
```sql
WITH T AS (
    SELECT
    P.party,
    Q.area,
    3 + (SUM((A.answer - 3.0) * Q.modifier) / COUNT(A.pol_id)) AS score
  FROM answers AS A
  JOIN questions AS Q ON Q.q_id = A.q_id
  JOIN politicians AS P ON P.id = A.pol_id
  WHERE Q.modifier <> 0
  GROUP BY 1, 2
)
SELECT
  P.party,
  (SELECT score FROM T WHERE T.party=P.party AND T.area='Užsienio ir gynybos politika') AS Defence,
  (SELECT score FROM T WHERE T.party=P.party AND T.area='Ekologija: gamta kaip išteklius – gamta kaip gyvybė Ašies') AS Eco,
  (SELECT score FROM T WHERE T.party=P.party AND T.area='Rinka ir valstybė: reguliuojama rinka – laisva rinka') AS Market,
  (SELECT score FROM T WHERE T.party=P.party AND T.area='Visuomenė: konservatyvumas - progresyvumas') AS Progresive
FROM (SELECT DISTINCT party FROM politicians) AS P;
```

---
Question area matrix by politicians:
```sql
WITH T AS (
    SELECT
    P.party,
    P.name,
    Q.area,
    3 + (SUM((A.answer - 3.0) * Q.modifier) / COUNT(A.pol_id)) AS score
  FROM answers AS A
  JOIN questions AS Q ON Q.q_id = A.q_id
  JOIN politicians AS P ON P.id = A.pol_id
  WHERE Q.modifier <> 0
  GROUP BY 1, 2, 3
)
SELECT
  P.party,
  P.name,
  (SELECT score FROM T WHERE T.party=P.party AND T.name=P.name AND T.area='Užsienio ir gynybos politika') AS Defence,
  (SELECT score FROM T WHERE T.party=P.party AND T.name=P.name AND T.area='Ekologija: gamta kaip išteklius – gamta kaip gyvybė Ašies') AS Eco,
  (SELECT score FROM T WHERE T.party=P.party AND T.name=P.name AND T.area='Rinka ir valstybė: reguliuojama rinka – laisva rinka') AS Market,
  (SELECT score FROM T WHERE T.party=P.party AND T.name=P.name AND T.area='Visuomenė: konservatyvumas - progresyvumas') AS Progresive
FROM politicians AS P;
```