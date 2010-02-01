namespace SkipBo
{
    public interface IPlayer
    {
        int GamesWon { get; }

        string GetName { get; }

        void Play(Board board);
        void WonGame();
    }
}