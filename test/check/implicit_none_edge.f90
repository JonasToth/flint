module mod_utility
!  implicit     none
contains
  subroutine locate
    ! implicit   is not   none
  end subroutine locate
  function equal(arg1,arg2) result(res)
    real(8), intent(in) :: arg1, arg2
    logical :: res
    res = (abs(arg1-arg2) < 0.02)
  end function equal
end module mod_utility

program my_program
  implicit none ! kajsd lja
end program my_program
