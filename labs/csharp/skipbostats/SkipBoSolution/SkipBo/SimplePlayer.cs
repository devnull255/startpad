using System;
using System.Collections.Generic;
using System.Text;

namespace SkipBo
{
    public class SimplePlayer : IPlayer
    {
        static private int _iNextPlayer = 1;
        private string _name;
        private int _gamesWon = 0;
        public int GamesWon
        {
            get { return _gamesWon;  }
        }

        public SimplePlayer() : this("SimplePlayer " + _iNextPlayer++)
        {
        }

        public SimplePlayer(string name)
        {
            _name = name;
        }

        public override string ToString()
        {
            return _name;
        }

        public string GetName
        {
            get { return _name; }
        }

        public virtual void Play(Board board)
        {
            bool hasPlayedCard;
            hasPlayedCard = PlayReserveCardToBuild(board) ||
                PlayCardFromHandToBuild(board) ||
                PlayFromDiscardPileToBuild(board);

            if (!hasPlayedCard && board.GetHand(this).Count != 0 && board.Winner == null)
                Discard(board);
        }

        private bool PlayFromDiscardPileToBuild(Board board)
        {
            foreach (Pile discardPile in board.GetDiscardPiles(this))
            {
                if (discardPile.HasCards)
                {
                    foreach (Pile buildPile in board.BuildPiles)
                    {
                        int playedValue;
                        if (buildPile.IsLegalPlay(discardPile.Top, buildPile, out playedValue))
                        {
                            discardPile.Top.PlayedValue = playedValue;
                            board.DoPlay(new Play(discardPile, buildPile));
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        private bool PlayCardFromHandToBuild(Board board)
        {
            foreach (Pile pile in board.BuildPiles)
            {
                Pile hand = board.GetHand(this);
                foreach (Card card in hand)
                {
                    int playedValue;
                    if (pile.IsLegalPlay(card, pile, out playedValue))
                    {
                        card.PlayedValue = playedValue;
                        board.DoPlay(new Play(hand, card, pile));
                        return true;
                    }
                }
            }
            return false;
        }

        private bool PlayReserveCardToBuild(Board board)
        {
            Card topReserveCard = board.GetReservePile(this).Top;
            foreach (Pile buildPile in board.BuildPiles)
            {
                int playedValue;
                if (buildPile.IsLegalPlay(topReserveCard, buildPile, out playedValue))
                {
                    board.GetReservePile(this).Top.PlayedValue = playedValue;
                    board.DoPlay(new Play(board.GetReservePile(this), buildPile));
                    return true;
                }
            }
            return false;
        }

        protected  void Discard(Board board)
        {
            // Select first card in hand and discard to random pile
            board.DoPlay(new Play(board.GetHand(this), board.GetDiscardPiles(this)[Utility.Random().Next(Board.NumDiscardPiles)]));
        }

        public void WonGame()
        {
            _gamesWon++;
        }
    }
}
