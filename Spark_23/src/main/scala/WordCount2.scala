/**
  * Created by Johnson on 上午10:17
  */
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.log4j.{Level,Logger}
// 引入处理日志的库
object WordCount2 {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("My First Spark APP")
    conf.setMaster("local")
    //    setting
    val sc = new SparkContext(conf)
    print("Success")

  }
}
