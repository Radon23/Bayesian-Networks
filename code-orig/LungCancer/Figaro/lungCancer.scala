import com.cra.figaro.language._
import com.cra.figaro.library.compound._
import com.cra.figaro.algorithm.factored.VariableElimination

object LungCancerInference {
  def main(args: Array[String]): Unit = {
    Universe.createNew()

    val pollution = Flip(0.1)
    val smoker = Flip(0.3)
  
    val lungCancer = CPD(pollution, smoker,
      (false, false) -> Flip(0.001),
      (false, true) -> Flip(0.03),
      (true, false) -> Flip(0.02),
      (true, true) -> Flip(0.05)
    )

    val xRay = If(lungCancer, Flip(0.9), Flip(0.2))
    val dyspnoea = If(lungCancer, Flip(0.65), Flip(0.30))

    val algorithm = VariableElimination(lungCancer)

    xRay.observe(true)
    dyspnoea.observe(true)

    algorithm.start()

    val poobabilityOfCancer = algorithm.probability(lungCancer, true)

    println("Probability of having lung cancer given xRay and dyspnoea: " + poobabilityOfCancer)

    algorithm.kill()
  }
}
