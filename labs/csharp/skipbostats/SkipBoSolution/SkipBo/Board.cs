

using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace SkipBo
{
    public class Board
    {
        // Todo:
        // SimplePlayer Winner()
        // Play enumerator

        public const int HandSize = 5;
        public const int NumDiscardPiles = 4;
        public const int NumBuildPiles = 4;
        public const int MaxPlayCount = 500;

        public const int SkipBos = 18;
        public const int CardUniqueValues = 12;
        public const int CardsPerValue = 12;
        public const int ReservePileMax = 25;
        public const int TotalCards = CardUniqueValues * CardsPerValue + SkipBos;

        private DrawPile _drawPile = new DrawPile();
        // The players list and player discard piles indexes must match
        private List<IPlayer> _players = new List<IPlayer>();
        private List<Pile> _buildPiles = new List<Pile>();
        private List<Pile> _playerHands = new List<Pile>();
        private List<Pile> _playerReservePile = new List<Pile>();
        private List<List<Pile>> _playerDiscardPiles = new List<List<Pile>>();
        private IPlayer _currentPlayer;
        private int _currentPlayerIndex = 0;
        private bool _isDiscarded = false;
        private bool _hasBeenFilled = false;

        private bool _isGameOver = false;
        private IPlayer _winner = null;
        public IPlayer Winner
        {
            get { return _winner; }
        }

        public bool IsGameOver
        {
            get { return _isGameOver; }
        }

        public Board()
        {
            InitDrawPile();
            ShufflePile(_drawPile);
            for (int i = 0; i < Board.NumBuildPiles; i++)
                _buildPiles.Add(new Pile(PileType.Build));
        }

        public void AddPlayer(IPlayer player)
        {
            _players.Add(player);
            _playerReservePile.Add(new Pile(PileType.Reserve));
            _playerHands.Add(new Pile(PileType.Hand));
            List<Pile> discardPiles = new List<Pile>();
            for (int index = 0; index < NumDiscardPiles; index++ )
            {
                discardPiles.Add(new Pile(PileType.Discard));
            }
            _playerDiscardPiles.Add(discardPiles);
            if (_currentPlayer == null)
                SetCurrentPlayer(player);
        }

        public int IndexOfPlayer(IPlayer player)
        {
            for (int indexOfPlayer = 0; indexOfPlayer < _players.Count; indexOfPlayer++)
            {
                if (_players[indexOfPlayer] == player)
                    return indexOfPlayer;
            }

            throw new ApplicationException("Trying to find player that doesn't exist");
        }
        public void SetCurrentPlayer(IPlayer player)
        {
            _currentPlayer = player;
            _currentPlayerIndex = IndexOfPlayer(player);
        }

        public IPlayer NextPlayer()
        {
            Logger.Write(string.Format("End of Play for {0}", _currentPlayer));
            Logger.Write("");
            _isDiscarded = false;
            _hasBeenFilled = false;
            _currentPlayerIndex++;
            if (_currentPlayerIndex == _players.Count)
                _currentPlayerIndex = 0;
            _currentPlayer = _players[_currentPlayerIndex];
            return _currentPlayer;
        }

        // BUG: how would I return a read-only version of a player to caller (protected).
        public IPlayer CurrentPlayer
        {
            get { return _currentPlayer; }
        }

        public IList<IPlayer> Players
        {
            get { return _players.AsReadOnly(); }
        }

        public DrawPile DrawPile
        {
            get { return _drawPile; }
        }

        private void InitDrawPile()
        {
            for (int cardIndex = 0; cardIndex < Board.CardUniqueValues; cardIndex++)
            {
                for (int cardValue = 1; cardValue <= Board.CardsPerValue; cardValue++)
                {
                    Card card = new Card(cardValue);
                    _drawPile.Add(card);
                }
            }

            for (int skipBoIndex = 0; skipBoIndex < Board.SkipBos; skipBoIndex++)
            {
                Card card = new Card(Card.SkipBoValue);
                _drawPile.Add(card);
            }
        }

        public void PrepGame()
        {
            for (int index = 0; index < _players.Count; index++ )
            {
                Pile reservePile = _playerReservePile[index];
                for (int cardIndex = 0; cardIndex < Board.ReservePileMax; cardIndex++)
                {
                    reservePile.Add(_drawPile.Pop());
                }
            }
        }

        public void PlayGame()
        {
            int iMax = 0;

            // BUG: Not correct termination for all games.
            while (iMax++ < MaxPlayCount && !_isGameOver)
            {
                PlayTurn();
            }
        }

        public void PlayTurn()
        {
            FillCurrentPlayersHand();

            while(!_isGameOver)
            {
                _currentPlayer.Play(this);
                if (Winner != null)
                {
                    return;
                }
                if (_isDiscarded)
                {
                    NextPlayer();
                    return;
                }
                if (GetHand(_currentPlayer).Count == 0)
                    FillCurrentPlayersHand();
            }
        }

        public Pile GetReservePile(IPlayer player)
        {
            int indexOfPlayer = IndexOfPlayer(player);
            return _playerReservePile[indexOfPlayer];
        }

        public List<Pile> GetDiscardPiles(IPlayer player)
        {
            return _playerDiscardPiles[IndexOfPlayer(player)];
        }

        public IList<Pile> BuildPiles
        {
            get { return _buildPiles.AsReadOnly(); }
        }

        public Pile GetHand(IPlayer player)
        {
            return _playerHands[IndexOfPlayer(player)];
        }

        public void FillCurrentPlayersHand()
        {
            Pile playerHand = GetHand(_currentPlayer);

            if (_hasBeenFilled && playerHand.Count != 0)
                throw new ApplicationException("Over-dealing cards to the same player.");

            while (playerHand.Count < Board.HandSize && _drawPile.Count > 0)
            {
                playerHand.Add(_drawPile.Pop());
            }

            _hasBeenFilled = true;

            if (playerHand.Count == 0)
                _isGameOver = true;

            Logger.Write(string.Format("{0} Reserve({1}):{2}", playerHand.ToString("P"), GetReservePile(CurrentPlayer).Count, GetReservePile(CurrentPlayer).Top));
        }

        // Execute a single-card play for the current player.
        public void DoPlay(Play play)
        {
            if (!play.IsValid())
                throw(new InvalidPlayException(play));

            if (_isDiscarded)
                throw (new ApplicationException("No more plays allowed after a discard."));

            if (_winner != null)
                throw (new ApplicationException("No more plays allowed after a winner."));

            Card cardFrom = PopCardFromPile(play.FromPile, play.FromCardIndex);

            play.ToPile.Add(cardFrom);
            if (play.ToPile.PileType == PileType.Build && play.ToPile.Count == Board.CardUniqueValues)
            {
                RecycleBuildPile(play.ToPile);
            }

            if (play.ToPileType == PileType.Discard)
                _isDiscarded = true;

            if (_playerReservePile[_currentPlayerIndex].Count == 0)
            {
                Logger.Write("Winner: " + _currentPlayer);
                _currentPlayer.WonGame();
                _winner = _currentPlayer;
                _isGameOver = true;
            }

        }

        private static Card PopCardFromPile(Pile fromPile, int index)
        {
            Card card = null;

            switch (fromPile.PileType)
            {
                case PileType.Build:
                    throw (new ApplicationException("Can't pop cards from Build pile"));
                case PileType.Discard:
                case PileType.Reserve:
                case PileType.Hand:
                    card = fromPile[index];
                    fromPile.Remove(card);
                    return card;
                 default:
                    throw new ApplicationException("Unhandled piletype " + fromPile.PileType);
            }
        }

        public List<Play> GetValidPlays()
        {
            List<Play> plays = new List<Play>();
            Pile hand = GetHand(CurrentPlayer);
            foreach (Card handCard in hand)
            {
                foreach (Pile discardPile in _playerDiscardPiles[_currentPlayerIndex])
                {
                    Play play = new Play(hand, handCard, discardPile);
                    plays.Add(play);
                }
            }
            return plays;
        }

        private void RecycleBuildPile(Pile pile)
        {
            ShufflePile(pile);
            _drawPile.AddRange(pile);
            pile.Clear();
        }

        private void ShufflePile(Pile pile)
        {
            for (int indexCard = _drawPile.Count-1; indexCard >= 1; indexCard--)
            {
                int swapIndex = Utility.Random().Next(indexCard);
                Card tempCard = _drawPile[indexCard];
                _drawPile[indexCard] = _drawPile[swapIndex];
                _drawPile[swapIndex] = tempCard;
            }
        }
    }
}
