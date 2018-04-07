module mod_utility
  use mod_constants

  implicit none

contains

  subroutine locate(l,n,array,var,pos)
    !> Search the index of given value in sorted 1D array of unique values.
    !>
    !> It uses a binary search algorithm.
    implicit none
    integer(int_p), intent(in) :: l !> Initial guess of lower limit.
    integer(int_p), intent(in) :: n !> Size of array.
    real(real_p), dimension(n), intent(in) :: array !> Sorted array to search.
    real(real_p), intent(in) :: var !> Value to find.
    integer(int_p), intent(out) :: pos !> Resulting index.


    integer(int_p) :: jl !> Lower limit.
    integer(int_p) :: jm !> Midpoint
    integer(int_p) :: ju !> Upper limit
    ! Initialize lower limit (L=0 FOR A NORMAL VECTOR!).
    jl=l
    ! Initialize upper limit.
    ju=jl+n+1
    ! If we are not yet done compute a midpoint.
    do while (ju-jl > 1)
      jm=(ju+jl)/2
      ! Replace either the lower limit or the upper limit.
      if((array(n) > array(1)).eqv.(var >= array(jm))) then
        jl=jm
      else
        ju=jm
      endif
    enddo
    pos=jl
    pos=max(l+1,pos)
    return
  end subroutine locate


  pure function equal(arg1,arg2) result(res)
      !> Returns whether the arguments are equal to machine precision
      real(real_p), intent(in) :: arg1, arg2
      logical :: res
      res = (abs(arg1-arg2) < REALTOL)
    end function equal


    pure function different(arg1,arg2) result(res)
      !> Returns whether the arguments are different to machine precision
      real(real_p), intent(in) :: arg1, arg2
      logical :: res
      res = .not. equal(arg1, arg2)
    end function different


  subroutine append_line(string,line)
    !> Append a trimmed line to a trimmed string ending with a LF character
    !>
    implicit none

    character(len=:), allocatable, intent(inout) :: string
    character(len=*), intent(in) :: line

    string = trim(string) // trim(adjustl(line)) // char(10)

  end subroutine append_line


  function substitute_string(string,find,replace) result(str)
    !> Replace all occurances of "find" with "replace" in "string"
    !>
    implicit none

    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: find
    character(len=*), intent(in) :: replace

    character(len=:), allocatable :: str

    integer(int_p) :: pos
    integer(int_p) :: lf, lmax, l, lcur

    str = string

    lf = len(find)
    lmax = len(string)

    l = 0
    do while(index(str,find) /= 0)
      pos = index(str,find)
      lcur = len(str)
      str = str(1:pos - 1) // replace // str(pos + lf:lcur)
      l = l + 1
      if (l > lmax) exit
    enddo

  end function substitute_string


  function next_line_from_file(file_unit, iostat, iomsg) result(line)
    !> Read an entire line from a file
    !>
    use, intrinsic :: iso_fortran_env, only: iostat_eor

    implicit none

    integer, intent(in) :: file_unit
    integer, intent(out) :: iostat
    character(len=*), intent(out) :: iomsg

    character(len=:), allocatable :: line

    character(len=256) :: buffer
    integer :: size           ! number of characters read from the file.

    line = ''
    do
      read (file_unit, '(A)', advance='NO', iostat=iostat, iomsg=iomsg, size=size)  &
          buffer
      if (iostat > 0) return      ! some sort of error.
      line = line // buffer(1:size)
      if (iostat < 0) then
        if (iostat == iostat_eor) iostat = 0
        return
      end if
    end do
  end function next_line_from_file

  subroutine print_assertion_error(filename, line, error_msg)
    implicit none

    character(len=*), intent(in) :: filename
    integer(int_p), intent(in)   :: line
    character(len=*), intent(in) :: error_msg
    character(len=10)            :: line_string

    write (line_string, '(I2)') line
    write (*,*) trim(filename) // ": " // trim(line_string) // ": " // trim(error_msg)
  end subroutine print_assertion_error

  function general_assertion(filename, line, condition, error_msg, strategy) result(res)
    !> Implement a small helper function to assert conditions and print
    !> an appropriate error or even stop the program.
    !>
    !> This function is used to implement `assert`, `expects` and `ensures`.
    !> :strategy: 0 = Crashing Program, 1 = Continue with Error Message
    implicit none

    character(len=*), intent(in)          :: filename
    integer(int_p), intent(in)            :: line
    logical, intent(in)                   :: condition
    character(len=*), intent(in)          :: error_msg
    integer(int_p), intent(in), optional  :: strategy
    logical                               :: res

    if (.NOT. condition) then
      if (present(strategy)) then
        ! End Program Execution with error message
        if (strategy == 0) then
          call print_assertion_error(filename, line, error_msg)
          stop
        ! Continue Program Execution but print only error message.
        else if (strategy == 1) then
          call print_assertion_error(filename, line, error_msg)
        endif
      ! Ending Program Execution is the default strategy.
      else
        call print_assertion_error(filename, line, error_msg)
        stop
      endif
    endif
    res = condition
  end function general_assertion

  subroutine assert(filename, line, condition, message, strategy)
    implicit none
    character(len=*), intent(in)           :: filename
    integer(int_p), intent(in)             :: line
    logical, intent(in)                    :: condition
    character(len=*), intent(in), optional :: message
    integer(int_p), intent(in), optional   :: strategy
    logical                                :: res

    if (present(strategy)) then
      if (present(message)) then
        res = general_assertion(filename, line, condition, &
                                trim("Assertion failed") // ": " // trim(message),&
                                strategy)
      else
        res = general_assertion(filename, line, condition, &
                                "Assertion failed", strategy)
      endif
    else 
      if (present(message)) then
        res = general_assertion(filename, line, condition, message)
      else
        res = general_assertion(filename, line, condition, "Assertion failed")
      endif
    endif
  end subroutine

  subroutine expects(filename, line, condition, message, strategy)
    implicit none
    character(len=*), intent(in)           :: filename
    integer(int_p), intent(in)             :: line
    logical, intent(in)                    :: condition
    character(len=*), intent(in), optional :: message
    integer(int_p), intent(in), optional   :: strategy
    logical                                :: res

    if (present(strategy)) then
      if (present(message)) then
        res = general_assertion(filename, line, condition, &
                                trim("Precondition failed") // ": " // trim(message),&
                                strategy)
      else
        res = general_assertion(filename, line, condition, &
                                "Precondition failed", strategy)
      endif
    else 
      if (present(message)) then
        res = general_assertion(filename, line, condition, message)
      else
        res = general_assertion(filename, line, condition, &
                                "Precondition failed")
      endif
    endif
  end subroutine

  subroutine ensures(filename, line, condition, message, strategy)
    implicit none
    character(len=*), intent(in)            :: filename
    integer(int_p), intent(in)              :: line
    logical, intent(in)                     :: condition
    character(len=*), intent(in), optional  :: message
    integer(int_p), intent(in), optional    :: strategy
    logical                                 :: res

    if (present(strategy)) then
      if (present(message)) then
        res = general_assertion(filename, line, condition, &
                                trim("Postcondition failed") // ": " // trim(message),&
                                strategy)
      else
        res = general_assertion(filename, line, condition, &
                                "Postcondition failed", strategy)
      endif
    else 
      if (present(message)) then
        res = general_assertion(filename, line, condition, message)
      else
        res = general_assertion(filename, line, condition, &
                                "Postcondition failed")
      endif
    endif
  end subroutine


  subroutine print_field_info(name,field)
    !> Print information about a field
    implicit none
    character(len=*), intent(in)           :: name
    real(real_p), dimension(:), intent(in) :: field

    write(*,'(3A)') 'Information about field ', name, ':'
    write(*,'(A,2ES22.15)') 'Min/Max: ', minval(field), maxval(field)

  end subroutine print_field_info


end module mod_utility
