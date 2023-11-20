import com.cra.figaro.language._
import com.cra.figaro.library.compound._
import com.cra.figaro.algorithm.factored.VariableElimination

object AllergyInference {
  def main(args: Array[String]): Unit = {
    Universe.createNew()

    val highPollen = Flip(0.7)
    val ateAllergicFood = Flip(0.9)

    val hasAllergy = Chain(highPollen, ateAllergicFood, (pollen: Boolean, food: Boolean) =>
      if (pollen || food) Select(0.9 -> true, 0.1 -> false)
      else Select(0.5 -> true, 0.5 -> false))

    val sneeze = If(hasAllergy, Flip(0.7), Flip(0.3))
    val rash = If(hasAllergy, Flip(0.9), Flip(0.1))

    val algorithm = VariableElimination(hasAllergy)

    sneeze.observe(true)
    rash.observe(true)

    algorithm.start()

    val probabilityOfAllergy = algorithm.probability(hasAllergy, true)

    println("Probability of having an allergy given sneezing and rash: " + probabilityOfAllergy)

    algorithm.kill()
  }
}
