using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using SkipBo;

namespace TestSkipBo
{
    /// <summary>
    /// Summary description for TestCard
    /// </summary>
    [TestClass]
    public class TestCard
    {
        public TestCard()
        {
            //
            // TODO: Add constructor logic here
            //
        }

        #region Additional test attributes
        //
        // You can use the following additional attributes as you write your tests:
        //
        // Use ClassInitialize to run code before running the first test in the class
        // [ClassInitialize()]
        // public static void MyClassInitialize(TestContext testContext) { }
        //
        // Use ClassCleanup to run code after all tests in a class have run
        // [ClassCleanup()]
        // public static void MyClassCleanup() { }
        //
        // Use TestInitialize to run code before running each test 
        // [TestInitialize()]
        // public void MyTestInitialize() { }
        //
        // Use TestCleanup to run code after each test has run
        // [TestCleanup()]
        // public void MyTestCleanup() { }
        //
        #endregion

        [TestMethod]
        public void NewCardTest()
        {
            Card card = new Card(1);
            Assert.AreEqual(1, card.Value);
            Assert.IsFalse(card.IsSkipBo);

            Card skipBo = new Card(Card.SkipBoValue);
            Assert.AreEqual(Card.SkipBoValue, skipBo.Value);
            Assert.IsTrue(skipBo.IsSkipBo);
        }

        [TestMethod, ExpectedException(typeof (InvalidCardException))]
        public void CardIndexTooSmallTest()
        {
            Card invalid = new Card(-1);
        }

        [TestMethod, ExpectedException(typeof(InvalidCardException))]
        public void CardIndexTooLargeTest()
        {
            Card invalid = new Card(13);
        }

        [TestMethod]
        public void PlaySkipBoAsTest()
        {
            Card skipbo = new Card(Card.SkipBoValue);
            skipbo.PlayedValue = 5;
            Assert.AreEqual(5, skipbo.PlayedValue, "Skipbo card not set to played value of 5");

            Card nonSkipbo = new Card(10);
            Assert.AreEqual(10, nonSkipbo.Value, "Non skipbo didn't take on value from constructor");
            Assert.AreEqual(nonSkipbo.Value, nonSkipbo.PlayedValue, "PlayedValue of non skipbo card doesn't have same value as Value");

        }
    }
}
