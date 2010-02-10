using System;
using System.Collections.Generic;
using System.Diagnostics;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using SkipBo;
using SkipBo.Players;

namespace TestSkipBo
{
    /// <summary>
    /// Summary description for UnitTest1
    /// </summary>
    [TestClass]
    public class TestBoard
    {
        public TestBoard()
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
        public void NewBoardTest()
        {
            Board board;
            board = new Board();
        }
        
        [TestMethod]
        public void AddPlayersTest()
        {
            Board board = new Board();
            IPlayer player1 = new SimplePlayer();
            IPlayer player2 = new SimplePlayer();
            board.AddPlayer(player1);
            board.AddPlayer(player2);

            Assert.IsNotNull(board.Players);
            Assert.AreEqual(2, board.Players.Count);

            Assert.AreEqual(player1, board.CurrentPlayer);
            board.NextPlayer();
            Assert.AreEqual(player2, board.CurrentPlayer);
            board.NextPlayer();
            Assert.AreEqual(player1, board.CurrentPlayer);
        }

        [TestMethod, ExpectedException(typeof(ApplicationException))]
        public void SetInvalidPlayerTest()
        {
            Board board = DiscardOnly2PlayerSetup();

            IPlayer unknownPlayer = new SimplePlayer();
            board.SetCurrentPlayer(unknownPlayer);
        }

        [TestMethod]
        public void BoardTest()
        {
            Board board = new Board();
            Assert.IsNotNull(board.DrawPile);
            Assert.AreEqual(Board.TotalCards, board.DrawPile.Count);
            AssertDrawPileHistogramCorrect(board);
        }

        [TestMethod]
        public void ShuffledDrawPileTest()
        {
            Board board = new Board();
            AssertDrawPileHistogramCorrect(board);
            AssertDrawPileIsRandom(board);
        }

        [TestMethod]
        public void PrepGameTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            AssertBoardValid(board);
        }

        private static void AssertFullDeck(Board board)
        {
            Histogram histogram = new Histogram();

            histogram.AddPile(board.DrawPile);

            foreach (IPlayer player in board.Players)
            {
                histogram.AddPile(board.GetReservePile(player));
                histogram.AddPile(board.GetHand(player));
                foreach (Pile pile in board.GetDiscardPiles(player))
                    histogram.AddPile(pile);
            }

            foreach (Pile pile in board.BuildPiles)
                histogram.AddPile(pile);

            histogram.AssertFullDeck();
        }

        private static void AssertBoardValid(Board board)
        {
            AssertFullDeck(board);

            foreach (IPlayer player in board.Players)
            {
                Assert.IsTrue(board.GetReservePile(player).Count <= Board.ReservePileMax, "Excessive reserve pile: " + board.GetReservePile(player).Count);
                Assert.AreEqual(Board.NumDiscardPiles, board.GetDiscardPiles(player).Count, "Wrong number of discard piles.");
                Assert.AreEqual(Board.NumBuildPiles, board.BuildPiles.Count, "Wrong number of build piles.");
            }
        }

        [TestMethod]
        public void DealTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();

            IPlayer player = board.CurrentPlayer;
            board.FillCurrentPlayersHand();

            Assert.AreEqual(Board.HandSize, board.GetHand(player).Count);

            AssertBoardValid(board);
        }

        [TestMethod]
        public void MakeOneMoveTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();

            IPlayer player = board.CurrentPlayer;
            board.PlayTurn();

            AssertBoardValid(board);
            AssertCardsInPiles(board.GetDiscardPiles(player), 1);
        }

        [TestMethod]
        public void PlayFromReservePileTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();

            board.FillCurrentPlayersHand();

            int reserveCards = board.GetReservePile(board.Players[0]).Count;
            int countOfBuildPiles = 0;
            foreach (Pile pile in board.GetDiscardPiles(board.Players[0]))
            {
                countOfBuildPiles += pile.Count;
            }
            
            board.DoPlay(new Play(board.GetReservePile(board.CurrentPlayer), board.BuildPiles[0]));

            Assert.AreEqual(reserveCards-1, board.GetReservePile(board.Players[0]).Count, "Should be one less reserve card after play from reserve pile");
            int countOfAllBuildPilesAfterPlay = 0;
            foreach (Pile pile in board.BuildPiles)
            {
                countOfAllBuildPilesAfterPlay += pile.Count;
            }
            Assert.AreEqual(countOfBuildPiles+1, countOfAllBuildPilesAfterPlay, "Build piles should have one more after playing");
        }


        [TestMethod, ExpectedException(typeof(InvalidPlayException))]
        public void PlayOffBuildPileTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            board.DoPlay(new Play(board.BuildPiles[0], board.GetDiscardPiles(board.CurrentPlayer)[0]));
        }

        [TestMethod, ExpectedException(typeof(ApplicationException))]
        public void TryToPlayAgainAfterDiscardTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            board.DoPlay(new Play(board.GetHand(board.CurrentPlayer), board.GetDiscardPiles(board.CurrentPlayer)[0]));
            board.DoPlay(new Play(board.GetHand(board.CurrentPlayer), board.GetDiscardPiles(board.CurrentPlayer)[0]));
        }

        [TestMethod]
        public void PlayBasicGame()
        {
            int maxPlays = 0;

            Board board = Default2PlayerSetup();
            board.PrepGame();

            while (board.DrawPile.Count > 0 && maxPlays++ < Board.MaxPlayCount && board.Winner == null)
            {
                board.PlayTurn();
                AssertBoardValid(board);
            }

            Assert.IsTrue(maxPlays <= Board.MaxPlayCount, "Too many plays - possible infinite loop.");
        }

        [TestMethod]
        public void PlayTillWinnerGameTest()
        {
            int maxPlays = 0;

            Board board = Default2PlayerSetup();
            board.PrepGame();

            while (board.Winner == null && maxPlays++ < Board.MaxPlayCount)
            {
                board.PlayTurn();
                AssertBoardValid(board);
            }

            Assert.IsNotNull(board.Winner, "Must have a winner");
            Assert.IsTrue(maxPlays <= Board.MaxPlayCount, "Too many plays - possible infinite loop.");
        }

        [TestMethod]
        public void PlayManyGamesTest()
        {
            IPlayer player1 = new SimplePlayer();
            IPlayer player2 = new DiscardOnlyPlayer();
            int NumDrawGames = 0;
            const int TotalGamesPlayed = 25;

            for (int gameNumber = 0; gameNumber < TotalGamesPlayed; gameNumber++)
            {
                Board board = new Board();
                board.AddPlayer(player1);
                board.AddPlayer(player2);

                board.PrepGame();
                board.PlayGame();

                if (board.Winner == null)
                    NumDrawGames++;
            }

            Debug.WriteLine(string.Format("{0} won {1}, {2} won {3}. {4} Drawn = Total {5}", player1, player1.GamesWon, player2, player2.GamesWon, NumDrawGames, TotalGamesPlayed));
            Assert.AreEqual(TotalGamesPlayed, NumDrawGames+player1.GamesWon + player2.GamesWon, "Total number of games won and drawn must match games played.");
        }

        [TestMethod]
        public void DiscardOnlyWithNoDrawShouldEmptyPlayerHandTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();

            // Get all cards out of players hands
            for (int i = 0; i < 10; i++)
            {
                if (board.GetHand(board.CurrentPlayer).Count > 0)
                {
                    board.PlayTurn();
                    AssertBoardValid(board);
                }
            }

            foreach (IPlayer player in board.Players)
            {
                Assert.AreEqual(0, board.GetHand(player).Count, "SimplePlayer " + player + "'s hand should be empty");
            }
        }

        [TestMethod]
        public void DoPlayTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            board.DoPlay(new Play(board.GetHand(board.CurrentPlayer), board.GetDiscardPiles(board.CurrentPlayer)[0]));
        }

        [TestMethod, ExpectedException(typeof(ApplicationException))]
        public void DoFillTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            board.DoPlay(new Play(board.GetHand(board.CurrentPlayer), board.GetDiscardPiles(board.CurrentPlayer)[0]));

            board.FillCurrentPlayersHand();

        }

        [TestMethod, ExpectedException(typeof(InvalidPlayException))]
        public void DoBadPlayTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            board.DoPlay(new Play(board.BuildPiles[0], board.GetDiscardPiles(board.CurrentPlayer)[0]));
        }

        [TestMethod]
        public void GamePlayTest()
        {
            Board board = Default2PlayerSetup();
            board.PrepGame();
            board.PlayGame();
            AssertBoardValid(board);
            Assert.IsTrue(board.Winner != null, "Expect a winner.");
        }


        [TestMethod]
        public void DrawGamePlayTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.PlayGame();
            AssertBoardValid(board);
            Assert.IsTrue(board.Winner == null && board.IsGameOver, "Expect a draw.");
        }

        [TestMethod, ExpectedException(typeof(InvalidPlayException))]
        public void InvalidPlayExceptionTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();
            try
            {
                board.DoPlay(new Play(board.BuildPiles[0], board.BuildPiles[1]));
            }
            catch (InvalidPlayException e)
            {
                Assert.IsTrue(e.Message.Contains("Invalid Play"), "Message " + e.Message + " wasn't expected");
                throw;
            }
        }

        [TestMethod]
        public void PlayGenerationTest()
        {
            Board board = DiscardOnly2PlayerSetup();
            board.PrepGame();
            board.FillCurrentPlayersHand();

            List<Play> plays = board.GetValidPlays();
            Assert.IsNotNull(plays, "Play was null");
            Assert.AreNotEqual(0, plays.Count, "No plays found!");
            Assert.IsTrue(plays[0].IsValid(), "Play is not valid.");

            int minPossiblePlays = board.GetHand(board.CurrentPlayer).Count*Board.NumDiscardPiles;
            int maxPossiblePlays = 60;
            Assert.IsTrue(minPossiblePlays <= plays.Count, "Has less than min possible plays returned.");
            Assert.IsTrue(maxPossiblePlays >= plays.Count, "Has more than max possible plays returned.");
        }

        private static void AssertCardsInPiles(List<Pile> piles, int expectedCardCount)
        {
            int totalCards = 0;
            foreach (Pile pile in piles)
            {
                totalCards += pile.Count;
            }

            Assert.AreEqual(expectedCardCount, totalCards, "Expected " + expectedCardCount + " cards but found " + totalCards);
        }

        #region Private Methods

        private static void AssertDrawPileIsRandom(Board board)
        {
            Card previousCard = null;
            RunCounter rcInc = new RunCounter();
            RunCounter rcDec = new RunCounter();
            RunCounter rcEqual = new RunCounter();

            foreach (Card card in board.DrawPile)
            {
                if (previousCard == null)
                {
                    rcInc.Extend(true);
                    rcDec.Extend(true);
                    rcEqual.Extend(true);
                }
                else
                {
                    rcInc.Extend(previousCard.Value == card.Value - 1);
                    rcDec.Extend(previousCard.Value == card.Value + 1);
                    rcEqual.Extend(previousCard.Value == card.Value);
                }
                
                previousCard = card;
            }

            Debug.WriteLine("DrawPile Max ascending sequence is " + rcInc.Max);
            Debug.WriteLine("DrawPile Max descending sequence is " + rcDec.Max);
            Debug.WriteLine("DrawPile Max equal sequence is " + rcEqual.Max);
            Debug.WriteLine("Deck is " + board.DrawPile);
            // Probability of 4 in a row is 1/12^4 or about one in 20,000 cards
            if (rcInc.Max > 4 || rcDec.Max > 4 || rcEqual.Max > 4)
            {
                Assert.Fail("DrawPile is not random.");
            }
        }

        private static void AssertDrawPileHistogramCorrect(Board board)
        {
            Histogram histogram = new Histogram();
            histogram.AddPile(board.DrawPile);
            histogram.AssertFullDeck();
        }

        private static Board DiscardOnly2PlayerSetup()
        {
            Board board = new Board();
            IPlayer player1 = new DiscardOnlyPlayer();
            IPlayer player2 = new DiscardOnlyPlayer();
            board.AddPlayer(player1);
            board.AddPlayer(player2);
            return board;
        }

        private static Board Default2PlayerSetup()
        {
            Board board = new Board();
            IPlayer player1 = new SimplePlayer();
            IPlayer player2 = new SimplePlayer();
            board.AddPlayer(player1);
            board.AddPlayer(player2);
            return board;
        }
        #endregion
    }

    public class RunCounter
    {
        private int cCur = 1;
        private int cMax = 1;

        public void Extend(bool f)
        {
            if (!f)
            {
                cCur = 1;
                return;
            }
    
            cCur++;
            if (cCur > cMax)
                cMax = cCur;
        }

         public int Max { get {return cMax;}}
    }

}
