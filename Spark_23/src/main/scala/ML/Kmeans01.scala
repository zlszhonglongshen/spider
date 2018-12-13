package ML
import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.{SparkContext,SparkConf}
/**
  * Created by Johnson on 上午11:11
  */
object Kmeans01 {
  def main(args: Array[String]): Unit = {
    if(args.length<1){
      System.err.println("Usage:<file>")
      System.exit(1)
    }
    val conf = new SparkConf()
    val sc = new SparkContext(conf)
    val data = sc.textFile(args(0))
    val parsedData = data.map(s => Vectors.dense(s.split(' ').map(_.toDouble)))
    val numClusters = 2
    val numIterations = 20
    val clusters = KMeans.train(parsedData,numClusters,numIterations)
    print("---Predict the existing line in the analyzed data file:"+args(0))
    print("Vector 1.0 2.1 3.8 belongs to clustering"+clusters.predict(Vectors.dense("1.0 2.1 3.8".split(" ").map(_.toDouble))))

    val wssse = clusters.computeCost(parsedData)
    print("Within set sum of Squared Errors="+wssse)
    sc.stop()
  }
}


/*
集群运行方式如下：

spark-submit --master spark://eb174:7077 --name WordCountByscala --class com.hq.WordCount --executor-memory 1G --total-executor-cores 2 ~/test/WordCount.jar hdfs://eb170:8020/user/ebupt/text
 */

