module mod_explicit
  implicit none
contains
  subroutine locate
    implicit none
  end subroutine locate

  function equal(arg1,arg2) result(res)
    implicit none
    real(8), intent(in) :: arg1, arg2
    logical :: res
    res = (abs(arg1-arg2) < 0.02)
  end function equal
end module mod_explicit

module mod_implicit
contains
  subroutine locate

  end subroutine locate

  function equal(arg1,arg2) result(res)
    real(8), intent(in) :: arg1, arg2
    logical :: res
    res = (abs(arg1-arg2) < 0.02)
  end function equal
end module mod_implicit

program my_program
  implicit none
end program my_program
program my_program2
end program my_program2
