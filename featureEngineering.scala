var df = spark.read
         .format("csv")
         .option("header", "true")
         .option("mode", "DROPMALFORMED")
         .load("data.csv")


// On rajoute une colonne heure H
df = df.withColumn("hour", split(col("datetime"), "\\ ").getItem(1))
df = df.withColumn("hour", split(col("hour"), "\\:").getItem(0))

// On rajoute une colonne jour du mois D
df = df.withColumn("day", split(col("datetime"), "\\ ").getItem(0))
df = df.withColumn("day", split(col("day"), "\\-").getItem(2))

// On rajoute une colonne jour de la semaine dow
import org.apache.spark.sql.functions.{from_unixtime, unix_timestamp}
df = df.withColumn("dow", col("datetime"))
df = df.withColumn("dow", from_unixtime(unix_timestamp($"dow", "yyyy-MM-dd"), "EEEEE"))

// On rajoute une colonne jour de l annee doy
df = df.withColumn("doy", col("datetime"))
df = df.withColumn("doy", dayofyear( from_unixtime(unix_timestamp($"doy", "yyyy-MM-dd") ) ) )

// On rajoute une colonne mois M
df = df.withColumn("month", split(col("datetime"), "\\ ").getItem(0))
df = df.withColumn("month", split(col("month"), "\\-").getItem(1))

// On rajoute une colonne annee Y
df = df.withColumn("year", split(col("datetime"), "-").getItem(0))

df.registerTempTable("bike")
df.printSchema()
df.write.format("csv")
        .option("header", "true")
        .save("dataV2.csv"
