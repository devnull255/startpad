using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using SkipBo;

namespace TestSkipBo
{
    /// <summary>
    /// Summary description for PlayerTest
    /// </summary>
    [TestClass]
    public class TestPlayer
    {
        public TestPlayer()
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

        /// <summary>
        ///A test for GetName
        ///</summary>
        [TestMethod()]
        public void GetNameTest()
        {
            IPlayer target = new SimplePlayer("Freddy");

            Assert.AreEqual("Freddy", target.GetName, "SkipBo.SimplePlayer.GetName was not set correctly.");
        }

        /// <summary>
        ///A test for GetName
        ///</summary>
        [TestMethod()]
        public void ToStringTest()
        {
            IPlayer target = new SimplePlayer();

            Assert.IsTrue(target.ToString().StartsWith("SimplePlayer "), "SkipBo.SimplePlayer.GetName was not set correctly.");
        }

        /// <summary>
        ///A test for SimplePlayer (string)
        ///</summary>
        [TestMethod()]
        public void PlayerConstructorTest()
        {
            IPlayer player1 = new SimplePlayer();
            Assert.IsTrue(player1.GetName.StartsWith("SimplePlayer "));
        }
    }
}
