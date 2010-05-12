using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using SkipBo;

namespace TestSkipBo
{
    /// <summary>
    /// Summary description for TestPlay
    /// </summary>
    [TestClass]
    public class TestPlay
    {
        public TestPlay()
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
        public void PlayValidityTest()
        {
            Pile discardPile = new Pile(PileType.Discard);
            Pile hand = new Pile(PileType.Hand);
            Pile reservePile = new Pile(PileType.Reserve);
            Pile drawPile = new Pile(PileType.Draw);
            Pile buildPile = new Pile(PileType.Build);

            Play play;

            Assert.IsTrue(Board.NumDiscardPiles == Board.NumDiscardPiles);
            for (int i = 0; i < Board.NumDiscardPiles; i++)
            {
                Card card = new Card(1);
                discardPile.Add(card);
                play = new Play(discardPile, buildPile);
                Assert.AreSame(card, play.PlayedCard, "Not expected PlayedCard");
                Assert.IsTrue(play.IsValid(), play.ToString());
            }

            Card handCard = new Card(1);
            hand.Add(handCard);
            play = new Play(hand, discardPile);
            Assert.IsTrue(play.ToString().Contains("->"));
            Assert.AreSame(handCard, play.PlayedCard, "Didn't play expected top hand card");
            Assert.IsTrue(play.IsValid(), play.ToString());

            Card reserveCard = new Card(1);
            reservePile.Add(reserveCard);
            play = new Play(reservePile, discardPile);
            Assert.AreSame(reserveCard, play.PlayedCard, "Didn't play expected top reserve card");
            Assert.IsFalse(play.IsValid(), play.ToString());

            Card buildCard = new Card(1);
            buildPile.Add(buildCard);
            play = new Play(buildPile, buildCard, discardPile);
            Assert.AreSame(buildCard, play.PlayedCard, "Didn't play expected top build card");
            Assert.IsFalse(play.IsValid(), play.ToString());

            Card drawCard = new Card(1);
            drawPile.Add(drawCard);
            play = new Play(drawPile, drawCard, hand);
            Assert.AreSame(drawCard, play.PlayedCard, "Didn't play expected draw card");
            Assert.IsTrue(play.IsValid(), string.Format("Draw->Hand should be valid: {0}", play));
        }

        [TestMethod]
        public void InvalidFromPileIndexTest()
        {
            Pile discardPile = new Pile(PileType.Discard);
            Pile hand = new Pile(PileType.Hand);
            Pile reservePile = new Pile(PileType.Reserve);
            Pile drawPile = new Pile(PileType.Draw);
            Pile buildPile = new Pile(PileType.Build);

            Card card = new Card(1);
            Play play = new Play(hand, card, buildPile);
            Assert.IsFalse(play.IsValid());

            hand.Add(card);
            play = new Play(hand, card, reservePile);
            Assert.IsFalse(play.IsValid());
        }

        [TestMethod]
        public void NewPlayTest()
        {
            Pile reservePile = new Pile(PileType.Reserve);
            reservePile.Add(new Card(1));
            Pile buildPile = new Pile(PileType.Build);

            Play play = new Play(reservePile, buildPile);
            Assert.IsTrue(play.IsValid(), "Play " + play + " should be valid");
        }
    }
}
