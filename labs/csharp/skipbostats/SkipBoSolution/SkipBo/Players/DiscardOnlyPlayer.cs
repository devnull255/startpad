namespace SkipBo.Players
{
    public class DiscardOnlyPlayer : SimplePlayer
    {
        public override void Play(Board board)
        {
            base.Discard(board);
        }
    }
}
